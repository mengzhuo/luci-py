#!/usr/bin/env python
# Copyright 2014 The Swarming Authors. All rights reserved.
# Use of this source code is governed by the Apache v2.0 license that can be
# found in the LICENSE file.

# Disable 'Method could be a function.'
# pylint: disable=R0201

import json
import sys
import unittest

import test_env
test_env.setup_test_env()

import webapp2
import webtest

from support import test_case
from components import utils

from components.auth import api
from components.auth import handler
from components.auth import model

from components.auth.ui import rest_api
from components.auth.ui import ui


def call_get(request_handler, expect_errors=False, uri=None):
  """Calls request_handler's 'get' in a context of webtest app."""
  uri = uri or '/dummy_path'
  assert uri.startswith('/')
  path = uri.rsplit('?', 1)[0]
  app = webtest.TestApp(webapp2.WSGIApplication([(path, request_handler)]))
  return app.get(uri, expect_errors=expect_errors)


def call_post(
    request_handler, body, content_type, expect_errors=False, uri=None):
  """Calls request_handler's 'post' in a context of webtest app."""
  uri = uri or '/dummy_path'
  assert uri.startswith('/')
  path = uri.rsplit('?', 1)[0]
  app = webtest.TestApp(webapp2.WSGIApplication([(path, request_handler)]))
  return app.post(
      uri, body, content_type=content_type, expect_errors=expect_errors)


def make_xsrf_token(identity=model.Anonymous, xsrf_token_data=None):
  """Returns XSRF token that can be used in tests."""
  # See handler.AuthenticatingHandler.generate
  return handler.XSRFToken.generate([identity.to_bytes()], xsrf_token_data)


def get_auth_db_rev():
  """Returns current version of AuthReplicationState.auth_db_rev."""
  ent = model.REPLICATION_STATE_KEY.get()
  return 0 if not ent else ent.auth_db_rev


def mock_replication_state(primary_url):
  """Modifies AuthReplicationState to represent Replica or Standalone modes."""
  if not primary_url:
    # Convert to standalone by nuking AuthReplicationState.
    model.REPLICATION_STATE_KEY.delete()
    assert model.is_standalone()
  else:
    # Convert to replica by writing AuthReplicationState with primary_id set.
    model.AuthReplicationState(
        key=model.REPLICATION_STATE_KEY,
        primary_id='mocked-primary',
        primary_url=primary_url).put()
    assert model.is_replica()


class ApiHandlerClassTest(test_case.TestCase):
  """Tests for ApiHandler base class itself."""

  def setUp(self):
    super(ApiHandlerClassTest, self).setUp()
    # Reset global config.
    handler.configure([])
    # Catch errors in log.
    self.errors = []
    self.mock(handler.logging, 'error',
        lambda *args, **kwargs: self.errors.append((args, kwargs)))

  def test_authentication_error(self):
    """AuthenticationErrors are returned as JSON with status 401."""
    test = self

    def failing_auth(_request):
      raise api.AuthenticationError('Boom!')
    handler.configure([failing_auth])

    class Handler(handler.ApiHandler):
      @api.public
      def get(self):
        test.fail('Should not be called')

    response = call_get(Handler, expect_errors=True)
    self.assertEqual(401, response.status_int)
    self.assertEqual(
        'application/json; charset=utf-8', response.headers.get('Content-Type'))
    self.assertEqual({'text': 'Boom!'}, json.loads(response.body))

  def test_authorization_error(self):
    """AuthorizationErrors are returned as JSON with status 403."""
    class Handler(handler.ApiHandler):
      @api.public
      def get(self):
        raise api.AuthorizationError('Boom!')

    response = call_get(Handler, expect_errors=True)
    self.assertEqual(403, response.status_int)
    self.assertEqual(
        'application/json; charset=utf-8', response.headers.get('Content-Type'))
    self.assertEqual({'text': 'Boom!'}, json.loads(response.body))

  def test_send_response_simple(self):
    class Handler(handler.ApiHandler):
      @api.public
      def get(self):
        self.send_response({'some': 'response'})

    response = call_get(Handler)
    self.assertEqual(200, response.status_int)
    self.assertEqual(
        'application/json; charset=utf-8', response.headers.get('Content-Type'))
    self.assertEqual({'some': 'response'}, json.loads(response.body))

  def test_send_response_custom_status_code(self):
    """Non 200 status codes in 'send_response' work."""
    class Handler(handler.ApiHandler):
      @api.public
      def get(self):
        self.send_response({'some': 'response'}, http_code=302)

    response = call_get(Handler)
    self.assertEqual(302, response.status_int)
    self.assertEqual(
        'application/json; charset=utf-8', response.headers.get('Content-Type'))
    self.assertEqual({'some': 'response'}, json.loads(response.body))

  def test_send_response_custom_header(self):
    """Response headers in 'send_response' work."""
    class Handler(handler.ApiHandler):
      @api.public
      def get(self):
        self.send_response({'some': 'response'}, headers={'Some-Header': '123'})

    response = call_get(Handler)
    self.assertEqual(200, response.status_int)
    self.assertEqual(
        'application/json; charset=utf-8', response.headers.get('Content-Type'))
    self.assertEqual(
        '123', response.headers.get('Some-Header'))
    self.assertEqual({'some': 'response'}, json.loads(response.body))

  def test_abort_with_error(self):
    """'abort_with_error' aborts execution and returns error as JSON."""
    test = self

    class Handler(handler.ApiHandler):
      @api.public
      def get(self):
        self.abort_with_error(http_code=404, text='abc', stuff=123)
        test.fail('Should not be called')

    response = call_get(Handler, expect_errors=True)
    self.assertEqual(404, response.status_int)
    self.assertEqual(
        'application/json; charset=utf-8', response.headers.get('Content-Type'))
    self.assertEqual({'text': 'abc', 'stuff': 123}, json.loads(response.body))

  def test_parse_body_success(self):
    """'parse_body' successfully decodes json-encoded dict in the body."""
    test = self

    class Handler(handler.ApiHandler):
      xsrf_token_enforce_on = ()
      @api.public
      def post(self):
        test.assertEqual({'abc': 123}, self.parse_body())

    response = call_post(
        Handler,
        json.dumps({'abc': 123}),
        'application/json; charset=utf-8')
    self.assertEqual(200, response.status_int)

  def test_parse_body_bad_content_type(self):
    """'parse_body' checks Content-Type header."""
    test = self

    class Handler(handler.ApiHandler):
      xsrf_token_enforce_on = ()
      @api.public
      def post(self):
        self.parse_body()
        test.fail('Request should have been aborted')

    response = call_post(
        Handler,
        json.dumps({'abc': 123}),
        'application/xml; charset=utf-8',
        expect_errors=True)
    self.assertEqual(400, response.status_int)

  def test_parse_body_bad_json(self):
    """'parse_body' returns HTTP 400 if body is not a valid json."""
    test = self

    class Handler(handler.ApiHandler):
      xsrf_token_enforce_on = ()
      @api.public
      def post(self):
        self.parse_body()
        test.fail('Request should have been aborted')

    response = call_post(
        Handler,
        'not-json',
        'application/json; charset=utf-8',
        expect_errors=True)
    self.assertEqual(400, response.status_int)

  def test_parse_body_not_dict(self):
    """'parse_body' returns HTTP 400 if body is not a json dict."""
    test = self

    class Handler(handler.ApiHandler):
      xsrf_token_enforce_on = ()
      @api.public
      def post(self):
        self.parse_body()
        test.fail('Request should have been aborted')

    response = call_post(
        Handler,
        '[]',
        'application/json; charset=utf-8',
        expect_errors=True)
    self.assertEqual(400, response.status_int)

  def test_parse_body_bad_encoding(self):
    test = self

    class Handler(handler.ApiHandler):
      xsrf_token_enforce_on = ()
      @api.public
      def post(self):
        self.parse_body()
        test.fail('Request should have been aborted')

    response = call_post(
        Handler,
        '[]',
        'application/json; charset=xmlcharrefreplace',
        expect_errors=True)
    self.assertEqual(400, response.status_int)


class RestAPITestCase(test_case.TestCase):
  """Test case for some concrete Auth REST API handler.

  Handler should be defined in get_rest_api_routes().
  """

  def setUp(self):
    super(RestAPITestCase, self).setUp()
    # Make webtest app that can execute REST API requests.
    self.app = webtest.TestApp(
        webapp2.WSGIApplication(rest_api.get_rest_api_routes(), debug=True))
    # Reset global config and cached state.
    handler.configure([])
    api.reset_local_state()
    self.mocked_identity = model.Anonymous
    # Catch errors in log.
    self.errors = []
    self.mock(handler.logging, 'error',
        lambda *args, **kwargs: self.errors.append((args, kwargs)))
    # Revision of AuthDB before the test. Used in tearDown().
    self._initial_auth_db_rev = get_auth_db_rev()
    self._auth_db_rev_inc = 0

  def tearDown(self):
    # Ensure auth_db_rev was changed expected number of times.
    try:
      self.assertEqual(
          self._initial_auth_db_rev + self._auth_db_rev_inc,
          get_auth_db_rev())
    finally:
      super(RestAPITestCase, self).tearDown()

  def expect_auth_db_rev_change(self, rev_inc=1):
    """Instruct tearDown to verify that auth_db_rev has changed."""
    self._auth_db_rev_inc += rev_inc

  def mock_current_identity(self, identity):
    """Makes api.get_current_identity() return predefined value."""
    self.mocked_identity = identity
    self.mock(api, 'get_current_identity', lambda: identity)

  def make_request(
      self,
      method,
      path,
      params=None,
      headers=None,
      expect_errors=False,
      expect_xsrf_token_check=False,
      expect_admin_check=False):
    """Sends a request to the app via webtest framework.

    Args:
      method: HTTP method of a request (like 'GET' or 'POST').
      path: request path.
      params: for GET, it's a query string, for POST/PUT its a body, etc. See
          webtest docs.
      headers: a dict with request headers.
      expect_errors: True if call is expected to end with some HTTP error code.
      expect_xsrf_token_check: if True, will append X-XSRF-Token header to the
          request and will verify that request handler checked it.
      expect_admin_check: if True, auth.is_admin is mocked to return True.

    Returns:
      Tuple (status code, deserialized JSON response, response headers).
    """
    # Add XSRF header if required.
    headers = dict(headers or {})
    if expect_xsrf_token_check:
      assert 'X-XSRF-Token' not in headers
      headers['X-XSRF-Token'] = make_xsrf_token(self.mocked_identity)

    # Hook XSRF token check to verify it's called.
    original_validate = handler.XSRFToken.validate
    xsrf_token_validate_calls = []
    def mocked_validate(*args, **kwargs):
      xsrf_token_validate_calls.append((args, kwargs))
      return original_validate(*args, **kwargs)
    self.mock(handler.XSRFToken, 'validate', staticmethod(mocked_validate))

    # Mock is_admin to return True.
    if expect_admin_check:
      original = api.is_group_member
      def is_group_member_mock(group, identity=None):
        return group == model.ADMIN_GROUP or original(group, identity)
      self.mock(api, 'is_group_member', is_group_member_mock)

    # Do the call. Pass |params| only if not None, otherwise use whatever
    # webtest method uses by default (for 'DELETE' it's something called
    # utils.NoDefault and it's treated differently from None).
    kwargs = {'headers': headers, 'expect_errors': expect_errors}
    if params is not None:
      kwargs['params'] = params
    response = getattr(self.app, method.lower())(path, **kwargs)

    # Ensure XSRF token was checked.
    if expect_xsrf_token_check:
      self.assertEqual(1, len(xsrf_token_validate_calls))

    # All REST API responses should be in JSON. Even errors. If content type
    # is not application/json, then response was generated by webapp2 itself,
    # show it in error message (it's usually some sort of error page).
    self.assertEqual(
        response.headers['Content-Type'],
        'application/json; charset=utf-8',
        msg=response.body)
    return response.status_int, json.loads(response.body), response.headers

  def get(self, path, **kwargs):
    """Sends GET request to REST API endpoint.

    Returns tuple (status code, deserialized JSON response, response headers).
    """
    return self.make_request('GET', path, **kwargs)

  def post(self, path, body=None, **kwargs):
    """Sends POST request to REST API endpoint.

    Returns tuple (status code, deserialized JSON response, response headers).
    """
    assert 'params' not in kwargs
    headers = dict(kwargs.pop('headers', None) or {})
    if body:
      headers['Content-Type'] = 'application/json; charset=utf-8'
    kwargs['headers'] = headers
    kwargs['params'] = json.dumps(body) if body is not None else ''
    return self.make_request('POST', path, **kwargs)

  def put(self, path, body=None, **kwargs):
    """Sends PUT request to REST API endpoint.

    Returns tuple (status code, deserialized JSON response, response headers).
    """
    assert 'params' not in kwargs
    headers = dict(kwargs.pop('headers', None) or {})
    if body:
      headers['Content-Type'] = 'application/json; charset=utf-8'
    kwargs['headers'] = headers
    kwargs['params'] = json.dumps(body) if body is not None else ''
    return self.make_request('PUT', path, **kwargs)

  def delete(self, path, **kwargs):
    """Sends DELETE request to REST API endpoint.

    Returns tuple (status code, deserialized JSON response, response headers).
    """
    return self.make_request('DELETE', path, **kwargs)


################################################################################
## Test cases for REST end points.


class SelfHandlerTest(RestAPITestCase):
  def test_anonymous(self):
    status, body, _ = self.get('/auth/api/v1/accounts/self')
    self.assertEqual(200, status)
    self.assertEqual({'identity': 'anonymous:anonymous'}, body)

  def test_non_anonymous(self):
    # Add fake authenticator.
    handler.configure([
        lambda _req: model.Identity(model.IDENTITY_USER, 'joe@example.com')])
    status, body, _ = self.get('/auth/api/v1/accounts/self')
    self.assertEqual(200, status)
    self.assertEqual({'identity': 'user:joe@example.com'}, body)


class XSRFHandlerTest(RestAPITestCase):
  def test_works(self):
    status, body, _ = self.post(
        path='/auth/api/v1/accounts/self/xsrf_token',
        headers={'X-XSRF-Token-Request': '1'})
    self.assertEqual(200, status)
    self.assertTrue(isinstance(body.get('xsrf_token'), basestring))

  def test_requires_header(self):
    status, body, _ = self.post(
        path='/auth/api/v1/accounts/self/xsrf_token',
        expect_errors=True)
    self.assertEqual(403, status)
    self.assertEqual({'text': 'Missing required XSRF request header'}, body)


class GroupsHandlerTest(RestAPITestCase):
  def test_requires_admin(self):
    status, body, _ = self.get('/auth/api/v1/groups', expect_errors=True)
    self.assertEqual(403, status)
    self.assertEqual({'text': 'Access is denied.'}, body)

  def test_empty_list(self):
    status, body, _ = self.get('/auth/api/v1/groups', expect_admin_check=True)
    self.assertEqual(200, status)
    self.assertEqual({'groups': []}, body)

  def test_non_empty_list(self):
    # Freeze time in NDB's |auto_now| properties.
    self.mock_now(utils.timestamp_to_datetime(1300000000000000))

    # Create a bunch of groups with all kinds of members.
    for i in xrange(0, 5):
      group = model.AuthGroup(
          key=model.group_key('Test group %d' % i),
          created_by=model.Identity.from_bytes('user:creator@example.com'),
          description='Group for testing, #%d' % i,
          modified_by=model.Identity.from_bytes('user:modifier@example.com'),
          members=[model.Identity.from_bytes('user:joe@example.com')],
          globs=[model.IdentityGlob.from_bytes('user:*@example.com')])
      group.put()

    # Group Listing should return all groups. Member lists should be omitted.
    # Order is alphabetical by name,
    status, body, _ = self.get('/auth/api/v1/groups', expect_admin_check=True)
    self.assertEqual(200, status)
    self.assertEqual(
      {
        'groups': [
          {
            'created_by': 'user:creator@example.com',
            'created_ts': 1300000000000000,
            'description': 'Group for testing, #%d' % i,
            'modified_by': 'user:modifier@example.com',
            'modified_ts': 1300000000000000,
            'name': 'Test group %d' % i,
          } for i in xrange(0, 5)
        ],
      }, body)


class GroupHandlerTest(RestAPITestCase):
  def test_get_missing(self):
    status, body, _ = self.get(
        path='/auth/api/v1/groups/a%20group',
        expect_errors=True,
        expect_admin_check=True)
    self.assertEqual(404, status)
    self.assertEqual({'text': 'No such group'}, body)

  def test_get_existing(self):
    # Freeze time in NDB's |auto_now| properties.
    self.mock_now(utils.timestamp_to_datetime(1300000000000000))

    # Create a group with all kinds of members.
    group = model.AuthGroup(
        key=model.group_key('A Group'),
        created_by=model.Identity.from_bytes('user:creator@example.com'),
        description='Group for testing',
        modified_by=model.Identity.from_bytes('user:modifier@example.com'),
        members=[model.Identity.from_bytes('user:joe@example.com')],
        globs=[model.IdentityGlob.from_bytes('user:*@example.com')])
    group.put()

    # Fetch it via API call.
    status, body, headers = self.get(
        path='/auth/api/v1/groups/A%20Group',
        expect_admin_check=True)
    self.assertEqual(200, status)
    self.assertEqual(
      {
        'group': {
          'created_by': 'user:creator@example.com',
          'created_ts': 1300000000000000,
          'description': 'Group for testing',
          'globs': ['user:*@example.com'],
          'members': ['user:joe@example.com'],
          'modified_by': 'user:modifier@example.com',
          'modified_ts': 1300000000000000,
          'name': 'A Group',
          'nested': [],
        },
      }, body)
    self.assertEqual(
        'Sun, 13 Mar 2011 07:06:40 -0000',
        headers['Last-Modified'])

  def test_get_requires_admin(self):
    status, body, _ = self.get(
        path='/auth/api/v1/groups/a%20group',
        expect_errors=True)
    self.assertEqual(403, status)
    self.assertEqual({'text': 'Access is denied.'}, body)

  def test_delete_existing(self):
    # Create a group.
    group = model.AuthGroup(key=model.group_key('A Group'))
    group.put()

    # Delete it via API.
    self.expect_auth_db_rev_change()
    status, body, _ = self.delete(
        path='/auth/api/v1/groups/A%20Group',
        expect_xsrf_token_check=True,
        expect_admin_check=True)
    self.assertEqual(200, status)
    self.assertEqual({'ok': True}, body)

    # It is gone.
    self.assertFalse(model.group_key('A Group').get())

  def test_delete_existing_with_condition_ok(self):
    # Create a group.
    group = model.AuthGroup(key=model.group_key('A Group'))
    group.put()

    # Delete it via API using passing If-Unmodified-Since condition.
    self.expect_auth_db_rev_change()
    status, body, _ = self.delete(
        path='/auth/api/v1/groups/A%20Group',
        headers={
          'If-Unmodified-Since': utils.datetime_to_rfc2822(group.modified_ts),
        },
        expect_xsrf_token_check=True,
        expect_admin_check=True)
    self.assertEqual(200, status)
    self.assertEqual({'ok': True}, body)

    # It is gone.
    self.assertFalse(model.group_key('A Group').get())

  def test_delete_existing_with_condition_fail(self):
    # Create a group.
    group = model.AuthGroup(key=model.group_key('A Group'))
    group.put()

    # Try to delete it via API using failing If-Unmodified-Since condition.
    status, body, _ = self.delete(
        path='/auth/api/v1/groups/A%20Group',
        headers={
          'If-Unmodified-Since': 'Sun, 1 Mar 1990 00:00:00 -0000',
        },
        expect_errors=True,
        expect_xsrf_token_check=True,
        expect_admin_check=True)
    self.assertEqual(412, status)
    self.assertEqual({'text': 'Group was modified by someone else'}, body)

    # It is still there.
    self.assertTrue(model.group_key('A Group').get())

  def test_delete_referenced_group(self):
    # Create a group.
    group = model.AuthGroup(key=model.group_key('A Group'))
    group.put()

    # Create another group that includes first one as nested.
    another = model.AuthGroup(
        key=model.group_key('Another group'),
        nested=['A Group'])
    another.put()

    # Try to delete it via API.
    status, body, _ = self.delete(
        path='/auth/api/v1/groups/A%20Group',
        expect_errors=True,
        expect_xsrf_token_check=True,
        expect_admin_check=True)
    self.assertEqual(409, status)
    self.assertEqual(
        {
          'text': 'Group is being referenced in other groups',
          'details': {
            'groups': ['Another group'],
          },
        }, body)

    # It is still there.
    self.assertTrue(model.group_key('A Group').get())

  def test_delete_missing(self):
    # Unconditionally deleting a group that's not there is ok.
    status, body, _ = self.delete(
        path='/auth/api/v1/groups/A Group',
        expect_xsrf_token_check=True,
        expect_admin_check=True)
    self.assertEqual(200, status)
    self.assertEqual({'ok': True}, body)

  def test_delete_missing_with_condition(self):
    # Deleting missing group with condition is a error.
    status, body, _ = self.delete(
        path='/auth/api/v1/groups/A%20Group',
        headers={
          'If-Unmodified-Since': 'Sun, 1 Mar 1990 00:00:00 -0000',
        },
        expect_errors=True,
        expect_xsrf_token_check=True,
        expect_admin_check=True)
    self.assertEqual(412, status)
    self.assertEqual({'text': 'Group was deleted by someone else'}, body)

  def test_delete_requires_admin(self):
    status, body, _ = self.delete(
        path='/auth/api/v1/groups/A Group',
        expect_errors=True,
        expect_xsrf_token_check=True)
    self.assertEqual(403, status)
    self.assertEqual({'text': 'Access is denied.'}, body)

  def test_post_success(self):
    frozen_time = utils.timestamp_to_datetime(1300000000000000)
    creator_identity = model.Identity.from_bytes('user:creator@example.com')

    # Freeze time in NDB's |auto_now| properties.
    self.mock_now(frozen_time)
    # get_current_identity is used for 'created_by' and 'modified_by'.
    self.mock_current_identity(creator_identity)

    # Create a group to act as a nested one.
    group = model.AuthGroup(key=model.group_key('Nested Group'))
    group.put()

    # Create the group using REST API.
    self.expect_auth_db_rev_change()
    status, body, headers = self.post(
        path='/auth/api/v1/groups/A%20Group',
        body={
          'description': 'Test group',
          'globs': ['user:*@example.com'],
          'members': ['bot:some-bot', 'user:some@example.com'],
          'name': 'A Group',
          'nested': ['Nested Group'],
        },
        expect_xsrf_token_check=True,
        expect_admin_check=True)
    self.assertEqual(201, status)
    self.assertEqual({'ok': True}, body)
    self.assertEqual(
        'Sun, 13 Mar 2011 07:06:40 -0000', headers['Last-Modified'])
    self.assertEqual(
        'http://localhost/auth/api/v1/groups/A%20Group', headers['Location'])

    # Ensure it's there and all fields are set.
    entity = model.group_key('A Group').get()
    self.assertTrue(entity)
    expected = {
      'created_by': model.Identity(kind='user', name='creator@example.com'),
      'created_ts': frozen_time,
      'description': 'Test group',
      'globs': [model.IdentityGlob(kind='user', pattern='*@example.com')],
      'members': [
        model.Identity(kind='bot', name='some-bot'),
        model.Identity(kind='user', name='some@example.com'),
      ],
      'modified_by': model.Identity(kind='user', name='creator@example.com'),
      'modified_ts': frozen_time,
      'nested': ['Nested Group']
    }
    self.assertEqual(expected, entity.to_dict())

  def test_post_minimal_body(self):
    # Posting just a name is enough to create an empty group.
    self.expect_auth_db_rev_change()
    status, body, _ = self.post(
        path='/auth/api/v1/groups/A%20Group',
        body={'name': 'A Group'},
        expect_xsrf_token_check=True,
        expect_admin_check=True)
    self.assertEqual(201, status)
    self.assertEqual({'ok': True}, body)

  def test_delete_external_fails(self):
    status, body, _ = self.delete(
        path='/auth/api/v1/groups/prefix/name',
        expect_errors=True,
        expect_xsrf_token_check=True,
        expect_admin_check=True)
    self.assertEqual(400, status)
    self.assertEqual({'text': 'External groups are not writable'}, body)

  def test_post_mismatching_name(self):
    # 'name' key and name in URL should match.
    status, body, _ = self.post(
        path='/auth/api/v1/groups/A%20Group',
        body={'name': 'Another name here'},
        expect_errors=True,
        expect_xsrf_token_check=True,
        expect_admin_check=True)
    self.assertEqual(400, status)
    self.assertEqual(
        {'text': 'Missing or mismatching group name in request body'}, body)

  def test_post_bad_body(self):
    # Posting invalid body ('members' should be a list, not a dict).
    status, body, _ = self.post(
        path='/auth/api/v1/groups/A%20Group',
        body={'name': 'A Group', 'members': {}},
        expect_errors=True,
        expect_xsrf_token_check=True,
        expect_admin_check=True)
    self.assertEqual(400, status)
    self.assertEqual(
        {
          'text':
            'Expecting a list or tuple for \'members\', got \'dict\' instead',
        },
        body)

  def test_post_already_exists(self):
    # Make a group first.
    group = model.AuthGroup(key=model.group_key('A Group'))
    group.put()

    # Now try to recreate it again via API. Should fail with HTTP 409.
    status, body, _ = self.post(
        path='/auth/api/v1/groups/A%20Group',
        body={'name': 'A Group'},
        expect_errors=True,
        expect_xsrf_token_check=True,
        expect_admin_check=True)
    self.assertEqual(409, status)
    self.assertEqual({'text': 'Such group already exists'}, body)

  def test_post_missing_nested(self):
    # Try to create a group that references non-existing nested group.
    status, body, _ = self.post(
        path='/auth/api/v1/groups/A%20Group',
        body={'name': 'A Group', 'nested': ['Missing group']},
        expect_errors=True,
        expect_xsrf_token_check=True,
        expect_admin_check=True)
    self.assertEqual(409, status)
    self.assertEqual(
      {
        'text': 'Referencing a nested group that doesn\'t exist',
        'details': {
          'missing': ['Missing group'],
        }
      }, body)

  def test_post_requires_admin(self):
    status, body, _ = self.post(
        path='/auth/api/v1/groups/A%20Group',
        body={'name': 'A Group'},
        expect_errors=True,
        expect_xsrf_token_check=True)
    self.assertEqual(403, status)
    self.assertEqual({'text': 'Access is denied.'}, body)

  def test_post_external_fails(self):
    status, body, _ = self.post(
        path='/auth/api/v1/groups/prefix/name',
        body={'name': 'prefix/name'},
        expect_errors=True,
        expect_xsrf_token_check=True,
        expect_admin_check=True)
    self.assertEqual(400, status)
    self.assertEqual({'text': 'External groups are not writable'}, body)

  def test_put_success(self):
    frozen_time = utils.timestamp_to_datetime(1300000000000000)
    creator_identity = model.Identity.from_bytes('user:creator@example.com')

    # Freeze time in NDB's |auto_now| properties.
    self.mock_now(frozen_time)
    # get_current_identity is used for 'created_by' and 'modified_by'.
    self.mock_current_identity(creator_identity)

    # Create a group to act as a nested one.
    nested = model.AuthGroup(key=model.group_key('Nested Group'))
    nested.put()

    # Create a group.
    group = model.AuthGroup(key=model.group_key('A Group'))
    group.put()

    # Update it via API.
    self.expect_auth_db_rev_change()
    status, body, headers = self.put(
        path='/auth/api/v1/groups/A%20Group',
        body={
          'description': 'Test group',
          'globs': ['user:*@example.com'],
          'members': ['bot:some-bot', 'user:some@example.com'],
          'name': 'A Group',
          'nested': ['Nested Group'],
        },
        expect_xsrf_token_check=True,
        expect_admin_check=True)
    self.assertEqual(200, status)
    self.assertEqual({'ok': True}, body)
    self.assertEqual(
        'Sun, 13 Mar 2011 07:06:40 -0000', headers['Last-Modified'])

    # Ensure it is updated.
    entity = model.group_key('A Group').get()
    self.assertTrue(entity)
    expected = {
      'created_by': None,
      'created_ts': frozen_time,
      'description': 'Test group',
      'globs': [model.IdentityGlob(kind='user', pattern='*@example.com')],
      'members': [
        model.Identity(kind='bot', name='some-bot'),
        model.Identity(kind='user', name='some@example.com'),
      ],
      'modified_by': model.Identity(kind='user', name='creator@example.com'),
      'modified_ts': frozen_time,
      'nested': ['Nested Group']
    }
    self.assertEqual(expected, entity.to_dict())

  def test_put_mismatching_name(self):
    # Create a group.
    group = model.AuthGroup(key=model.group_key('A Group'))
    group.put()

    # Update it via API, pass bad name.
    status, body, _ = self.put(
        path='/auth/api/v1/groups/A%20Group',
        body={
          'description': 'Test group',
          'globs': [],
          'members': [],
          'name': 'Bad group name',
        },
        expect_errors=True,
        expect_xsrf_token_check=True,
        expect_admin_check=True)
    self.assertEqual(400, status)
    self.assertEqual(
        {'text': 'Missing or mismatching group name in request body'}, body)

  def test_put_bad_body(self):
    # Create a group.
    group = model.AuthGroup(key=model.group_key('A Group'))
    group.put()

    # Update it via API, pass a bad body ('globs' should be a list, not a dict).
    status, body, _ = self.put(
        path='/auth/api/v1/groups/A%20Group',
        body={
          'description': 'Test group',
          'globs': {},
          'members': [],
          'name': 'A Group',
        },
        expect_errors=True,
        expect_xsrf_token_check=True,
        expect_admin_check=True)
    self.assertEqual(400, status)
    self.assertEqual(
        {
          'text':
            'Expecting a list or tuple for \'globs\', got \'dict\' instead'
        }, body)

  def test_put_missing(self):
    # Try to update a group that doesn't exist.
    status, body, _ = self.put(
        path='/auth/api/v1/groups/A%20Group',
        body={
          'description': 'Test group',
          'globs': [],
          'members': [],
          'name': 'A Group',
          'nested': [],
        },
        expect_errors=True,
        expect_xsrf_token_check=True,
        expect_admin_check=True)
    self.assertEqual(404, status)
    self.assertEqual({'text': 'No such group'}, body)

  def test_put_bad_precondition(self):
    # Freeze time in NDB's |auto_now| properties.
    self.mock_now(utils.timestamp_to_datetime(1300000000000000))

    # Create a group.
    group = model.AuthGroup(key=model.group_key('A Group'))
    group.put()

    # Try to update it. Pass incorrect If-Modified-Since header.
    status, body, _ = self.put(
        path='/auth/api/v1/groups/A%20Group',
        body={
          'description': 'Test group',
          'globs': [],
          'members': [],
          'name': 'A Group',
          'nested': [],
        },
        headers={
          'If-Unmodified-Since': 'Sun, 1 Mar 1990 00:00:00 -0000',
        },
        expect_errors=True,
        expect_xsrf_token_check=True,
        expect_admin_check=True)
    self.assertEqual(412, status)
    self.assertEqual({'text': 'Group was modified by someone else'}, body)

  def test_put_missing_nested(self):
    # Create a group.
    group = model.AuthGroup(key=model.group_key('A Group'))
    group.put()

    # Try to update it. Pass missing group as a nested group.
    status, body, _ = self.put(
        path='/auth/api/v1/groups/A%20Group',
        body={
          'description': 'Test group',
          'globs': [],
          'members': [],
          'name': 'A Group',
          'nested': ['Missing group'],
        },
        expect_errors=True,
        expect_xsrf_token_check=True,
        expect_admin_check=True)
    self.assertEqual(409, status)
    self.assertEqual(
        {
          'text': 'Referencing a nested group that doesn\'t exist',
          'details': {'missing': ['Missing group']},
        }, body)

  def test_put_dependency_cycle(self):
    # Create a group.
    group = model.AuthGroup(key=model.group_key('A Group'))
    group.put()

    # Try to update it. Reference itself as a nested group.
    status, body, _ = self.put(
        path='/auth/api/v1/groups/A%20Group',
        body={
          'description': 'Test group',
          'globs': [],
          'members': [],
          'name': 'A Group',
          'nested': ['A Group'],
        },
        expect_errors=True,
        expect_xsrf_token_check=True,
        expect_admin_check=True)
    self.assertEqual(409, status)
    self.assertEqual(
        {
          'text': 'Groups can not have cyclic dependencies',
          'details': {'cycle': ['A Group']},
        }, body)

  def test_put_requires_admin(self):
    status, body, _ = self.put(
        path='/auth/api/v1/groups/A%20Group',
        body={},
        expect_errors=True,
        expect_xsrf_token_check=True)
    self.assertEqual(403, status)
    self.assertEqual({'text': 'Access is denied.'}, body)

  def test_put_external_fails(self):
    status, body, _ = self.post(
        path='/auth/api/v1/groups/prefix/name',
        body={'name': 'prefix/name'},
        expect_errors=True,
        expect_xsrf_token_check=True,
        expect_admin_check=True)
    self.assertEqual(400, status)
    self.assertEqual({'text': 'External groups are not writable'}, body)


class CertificatesHandlerTest(RestAPITestCase):
  def test_works(self):
    # Test mostly for code coverage.
    self.mock_now(utils.timestamp_to_datetime(1300000000000000))
    status, body, _ = self.get('/auth/api/v1/server/certificates')
    self.assertEqual(200, status)
    self.assertEqual(1300000000000000, body['timestamp'])
    self.assertTrue(body['certificates'])
    for cert in body['certificates']:
      self.assertTrue(isinstance(cert['key_name'], basestring))
      self.assertTrue(isinstance(cert['x509_certificate_pem'], basestring))


class OAuthConfigHandlerTest(RestAPITestCase):
  def test_non_configured_works(self):
    expected = {
      'additional_client_ids': [],
      'client_id': '',
      'client_not_so_secret': '',
      'primary_url': None,
    }
    status, body, _ = self.get('/auth/api/v1/server/oauth_config')
    self.assertEqual(200, status)
    self.assertEqual(expected, body)

  def test_primary_url_is_set_on_replica(self):
    mock_replication_state('https://primary-url')
    expected = {
      'additional_client_ids': [],
      'client_id': '',
      'client_not_so_secret': '',
      'primary_url': 'https://primary-url',
    }
    status, body, _ = self.get('/auth/api/v1/server/oauth_config')
    self.assertEqual(200, status)
    self.assertEqual(expected, body)

  def test_configured_works(self):
    # Mock auth_db.get_oauth_config().
    fake_config = model.AuthGlobalConfig(
        oauth_client_id='some-client-id',
        oauth_client_secret='some-secret',
        oauth_additional_client_ids=['a', 'b', 'c'])
    self.mock(rest_api.api, 'get_request_auth_db',
        lambda: api.AuthDB(global_config=fake_config))
    # Call should return this data.
    expected = {
      'additional_client_ids': ['a', 'b', 'c'],
      'client_id': 'some-client-id',
      'client_not_so_secret': 'some-secret',
      'primary_url': None,
    }
    status, body, _ = self.get('/auth/api/v1/server/oauth_config')
    self.assertEqual(200, status)
    self.assertEqual(expected, body)

  def test_no_cache_works(self):
    # Put something into DB.
    config_in_db = model.AuthGlobalConfig(
        key=model.ROOT_KEY,
        oauth_client_id='config-from-db',
        oauth_client_secret='some-secret-db',
        oauth_additional_client_ids=['a', 'b'])
    config_in_db.put()

    # Put another version into auth DB cache.
    config_in_cache = model.AuthGlobalConfig(
        oauth_client_id='config-from-cache',
        oauth_client_secret='some-secret-cache',
        oauth_additional_client_ids=['c', 'd'])
    self.mock(rest_api.api, 'get_request_auth_db',
        lambda: api.AuthDB(global_config=config_in_cache))

    # Without cache control header a cached version is used.
    expected = {
      'additional_client_ids': ['c', 'd'],
      'client_id': 'config-from-cache',
      'client_not_so_secret': 'some-secret-cache',
      'primary_url': None,
    }
    status, body, _ = self.get('/auth/api/v1/server/oauth_config')
    self.assertEqual(200, status)
    self.assertEqual(expected, body)

    # With cache control header a version from DB is used.
    expected = {
      'additional_client_ids': ['a', 'b'],
      'client_id': 'config-from-db',
      'client_not_so_secret': 'some-secret-db',
      'primary_url': None,
    }
    status, body, _ = self.get(
        path='/auth/api/v1/server/oauth_config',
        headers={'Cache-Control': 'no-cache'})
    self.assertEqual(200, status)
    self.assertEqual(expected, body)

  def test_post_works(self):
    # Send POST.
    request_body = {
      'additional_client_ids': ['1', '2', '3'],
      'client_id': 'some-client-id',
      'client_not_so_secret': 'some-secret',
    }
    self.expect_auth_db_rev_change()
    status, response, _ = self.post(
        path='/auth/api/v1/server/oauth_config',
        body=request_body,
        headers={'X-XSRF-Token': make_xsrf_token()},
        expect_admin_check=True)
    self.assertEqual(200, status)
    self.assertEqual({'ok': True}, response)

    # Ensure it modified the state in DB.
    config = model.ROOT_KEY.get()
    self.assertEqual('some-client-id', config.oauth_client_id)
    self.assertEqual('some-secret', config.oauth_client_secret)
    self.assertEqual(['1', '2', '3'], config.oauth_additional_client_ids)

  def test_post_requires_admin(self):
    status, response, _ = self.post(
        path='/auth/api/v1/server/oauth_config',
        body={},
        headers={'X-XSRF-Token': make_xsrf_token()},
        expect_errors=True)
    self.assertEqual(403, status)
    self.assertEqual({'text': 'Access is denied.'}, response)


class ServerStateHandlerTest(RestAPITestCase):
  def test_works(self):
    self.mock_now(utils.timestamp_to_datetime(1300000000000000))

    # Configure as standalone.
    state = model.AuthReplicationState(key=model.REPLICATION_STATE_KEY)
    state.put()

    expected = {
      'mode': 'standalone',
      'replication_state': {
        'auth_db_rev': 0,
        'modified_ts': 1300000000000000,
        'primary_id': None,
        'primary_url': None,
      }
    }
    status, body, _ = self.get(
        '/auth/api/v1/server/state', expect_admin_check=True)
    self.assertEqual(200, status)
    self.assertEqual(expected, body)


class ForbidApiOnReplicaTest(test_case.TestCase):
  """Tests for rest_api.forbid_api_on_replica decorator."""

  def test_allowed_on_non_replica(self):
    class Handler(webapp2.RequestHandler):
      @rest_api.forbid_api_on_replica
      def get(self):
        self.response.write('ok')

    mock_replication_state(None)
    self.assertEqual('ok', call_get(Handler).body)

  def test_forbidden_on_replica(self):
    calls = []

    class Handler(webapp2.RequestHandler):
      @rest_api.forbid_api_on_replica
      def get(self):
        calls.append(1)

    mock_replication_state('http://locahost:1234')
    response = call_get(Handler, expect_errors=True)

    self.assertEqual(0, len(calls))
    self.assertEqual(405, response.status_code)
    expected = {
      'primary_url': 'http://locahost:1234',
      'text': 'Use Primary service for API requests',
    }
    self.assertEqual(expected, json.loads(response.body))


class ForbidUiOnReplicaTest(test_case.TestCase):
  """Tests for ui.forbid_ui_on_replica decorator."""

  def test_allowed_on_non_replica(self):
    class Handler(webapp2.RequestHandler):
      @ui.forbid_ui_on_replica
      def get(self):
        self.response.write('ok')

    mock_replication_state(None)
    self.assertEqual('ok', call_get(Handler).body)

  def test_forbidden_on_replica(self):
    calls = []

    class Handler(webapp2.RequestHandler):
      @ui.forbid_ui_on_replica
      def get(self):
        calls.append(1)

    mock_replication_state('http://locahost:1234')
    response = call_get(Handler, expect_errors=True)

    self.assertEqual(0, len(calls))
    self.assertEqual(405, response.status_code)
    self.assertEqual(
        '405 Method Not Allowed\n\n'
        'The method GET is not allowed for this resource. \n\n '
        'Now allowed on a replica, see primary at http://locahost:1234',
        response.body)


class RedirectUiOnReplicaTest(test_case.TestCase):
  """Tests for ui.redirect_ui_on_replica decorator."""

  def test_allowed_on_non_replica(self):
    class Handler(webapp2.RequestHandler):
      @ui.redirect_ui_on_replica
      def get(self):
        self.response.write('ok')

    mock_replication_state(None)
    self.assertEqual('ok', call_get(Handler).body)

  def test_redirects_on_replica(self):
    calls = []

    class Handler(webapp2.RequestHandler):
      @ui.redirect_ui_on_replica
      def get(self):
        calls.append(1)

    mock_replication_state('http://locahost:1234')
    response = call_get(Handler, expect_errors=True, uri='/some/method?arg=1')

    self.assertEqual(0, len(calls))
    self.assertEqual(302, response.status_code)
    self.assertEqual(
        'http://locahost:1234/some/method?arg=1', response.headers['Location'])


if __name__ == '__main__':
  if '-v' in sys.argv:
    unittest.TestCase.maxDiff = None
  unittest.main()
