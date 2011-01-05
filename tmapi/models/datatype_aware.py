from django.db import models

from locator import Locator
from scoped import Scoped


class DatatypeAware (Scoped):

    """Common base interface for `Occurrence`s and `Variant`s."""
    
    datatype = models.CharField(max_length=512, blank=True)
    value = models.TextField()

    class Meta:
        abstract = True
        app_label = 'tmapi'

    def get_datatype (self):
        """Returns the `Locator` identifying the datatype of the value.

        :rtype: `Locator`

        """
        return Locator(self.datatype)
        
    def get_value (self):
        """Returns the lexical representation of the value."""
        return self.value

    def set_value (self, value):
        """Sets the string value."""
        raise Exception('Not yet implemented')
