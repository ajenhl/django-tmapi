# Copyright 2011 Jamie Norrish (jamie@artefact.org.nz)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.db import models

from tmapi.exceptions import ModelConstraintException

from .construct import Construct


class Reifiable (Construct, models.Model):

    """Indicates that a `Construct` is reifiable. Every Topic Maps
    construct that is not a `Topic` is reifiable."""

    reifier = models.OneToOneField('Topic', related_name='reified_%(class)s',
                                   null=True)

    class Meta:
        abstract = True
        app_label = 'tmapi'

    def get_reifier (self):
        """Returns the reifier of this construct.

        :rtype: `Topic`

        """
        return self.reifier

    def set_reifier (self, reifier):
        """Sets the reifier of this consutrct.

        The specified reifier **must not** reify another information
        item.

        :param reifier: the topic that should reify this construct or
          None if an existing reifier should be removed
        :type reifier: `Topic` or None
        :raises `ModelConstraintException`: if the specified `reifier`
          reifies another construct

        """
        if reifier is None:
            reified = None
        else:
            if self.get_topic_map() != reifier.topic_map:
                raise ModelConstraintException(
                    self, 'The reifier is not from the same topic map')
            reified = reifier.get_reified()
        if reified is None:
            self.reifier = reifier
            self.save()
        elif reified == self:
            pass
        else:
            raise ModelConstraintException(
                self, 'The reifier already reifies another construct')
