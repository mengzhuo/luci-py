# Copyright 2013 The Swarming Authors. All rights reserved.
# Use of this source code is governed by the Apache v2.0 license that can be
# found in the LICENSE file.

"""This file is meant to be overriden by the server's specific copy.

You can upload a new version via /restricted/upload/bot_config.

There's 3 types of functions in this file:
  - get_*() to return properties to describe this bot.
  - on_*() as hooks based on events happening on the bot.
  - setup_*() to setup global state on the host.

This file shouldn't import from other scripts in this directory except
os_utilities which is guaranteed to be usable as an API. It's fine to import
from stdlib.
"""

import os_utilities

# Unused argument 'bot' - pylint: disable=W0613


def get_dimensions():
  """Returns dict with the bot's dimensions.

  The dimensions are what are used to select the bot that can run each task.

  The bot id will be automatically selected based on the hostname with
  os_utilities.get_dimensions(). If you want something more special, specify it
  in your bot_config.py and override the item 'id'.
  """
  return os_utilities.get_dimensions()


def get_state():
  """Returns dict with a state of the bot reported to the server with each poll.

  It is only for dynamic state that changes while bot is running for information
  for the sysadmins.

  The server can not use this state for immediate scheduling purposes (use
  'dimensions' for that), but it can use it for maintenance and bookkeeping
  tasks.
  """
  return os_utilities.get_state()


### Hooks


def on_after_task(bot, failure, internal_failure):
  """Hook function to be called after running a task.

  It is an excellent place to do post-task cleanup of temporary files.

  The default implementation restarts after a task failure or an internal
  failure.

  Arguments:
  - bot: bot.Bot instance.
  - failure: bool, True if the task failed.
  - internal_failure: bool, True if an internal failure happened.
  """
  # Example code:
  #if failure:
  #  bot.restart('Task failure')
  #elif internal_failure:
  #  bot.restart('Internal failure')


### Setup


def setup_bot(bot):
  """Does one time initialization for this bot.

  Returns True if it's fine to start the bot right away. Otherwise, the calling
  script should exit.

  Example: making this script starts automatically on user login via
  os_utilities.set_auto_startup_win() or os_utilities.set_auto_startup_osx().
  """
  return True
