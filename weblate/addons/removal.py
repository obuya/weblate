# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2019 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <https://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from __future__ import unicode_literals

from datetime import timedelta

from django.db.models import Q, Sum
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from weblate.addons.base import BaseAddon
from weblate.addons.events import EVENT_DAILY
from weblate.addons.forms import RemoveForm, RemoveSuggestionForm


class RemovalAddon(BaseAddon):
    project_scope = True
    events = (EVENT_DAILY,)
    settings_form = RemoveForm
    icon = 'trash'

    def get_cutoff(self):
        age = self.instance.configuration['age']
        return timezone.now() - timedelta(days=age)

    def delete_older(self, objects):
        objects.filter(timestamp__lt=self.get_cutoff()).delete()


class RemoveComments(RemovalAddon):
    name = 'weblate.removal.comments'
    verbose = _('Stale comment removal')
    description = _('Set timeframe for removal of comments.')

    def daily(self, component):
        self.delete_older(
            component.project.comment_set.all()
        )


class RemoveSuggestions(RemovalAddon):
    name = 'weblate.removal.suggestions'
    verbose = _('Stale suggestion removal')
    description = _('Set timeframe for removal of suggestions.')
    settings_form = RemoveSuggestionForm

    def daily(self, component):
        self.delete_older(
            component.project.suggestion_set.annotate(
                Sum('vote__value')
            ).filter(
                Q(vote__value__sum__lte=self.instance.configuration.get('votes', 0))
                | Q(vote__value__sum=None)
            )
        )