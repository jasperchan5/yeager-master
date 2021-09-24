# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

# """linebot.models.send_messages module."""

from linebot.models import *

from __future__ import unicode_literals

from abc import ABCMeta

from future.utils import with_metaclass

from .actions import get_action
from .base import Base


class SendMessage(with_metaclass(ABCMeta, Base)):
    # """Abstract Base Class of SendMessage."""

    def __init__(self, quick_reply=None, sender=None, **kwargs):
        # """__init__ method.

        # :param quick_reply: QuickReply object
        # :type quick_reply: T <= :py:class:`linebot.models.send_messages.QuickReply`
        # :param sender: Sender object
        # :type sender: T <= :py:class:`linebot.models.send_messages.Sender`
        # :param kwargs:
        # """
        super(SendMessage, self).__init__(**kwargs)

        self.type = None
        self.quick_reply = self.get_or_new_from_json_dict(quick_reply, QuickReply)
        self.sender = self.get_or_new_from_json_dict(sender, Sender)

class CustomTypeSendMessage(SendMessage):

    def __init__(self, text=None, emojis=None, original_content_url=None, preview_image_url=None, quick_reply=None, **kwargs):
        if original_content_url != None:
            super(CustomTypeSendMessage, self).__init__(quick_reply=quick_reply, **kwargs)
            self.type = 'image'
            self.original_content_url = original_content_url
            self.preview_image_url = preview_image_url
        elif text != None:
            super(CustomTypeSendMessage, self).__init__(quick_reply=quick_reply, **kwargs)
            self.type = 'text'
            self.text = text
            self.emojis = emojis