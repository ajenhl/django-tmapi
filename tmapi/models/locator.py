import unicodedata
from urllib import quote, unquote


class LocatorBase (object):

    """Immutable representation of an IRI."""

    def generate_forms (self, reference):
        self._reference = self.unnormalise(reference)
        self._external = self.normalise(self._reference)
        
    def get_reference (self):
        """Returns a lexical representation of the IRI.

        :rtype: String

        """
        return self._reference

    def to_external_form (self):
        """Returns the external form of the IRI.

        Any special character will be escaped using the escaping
        conventions of RFC 3987.

        :rtype: String

        """
        return self._external

    def normalise (self, reference):
        reference = unicode(quote(reference), 'utf-8', 'replace')
        return reference
    
    def unnormalise (self, reference):
        if not isinstance(reference, unicode):
            reference = unicode(unquote(reference), 'utf-8', 'replace')
        else:
            reference = unquote(reference)
        return unicodedata.normalize('NFC', reference).encode('utf-8')

    def __eq__ (self, other):
        if not isinstance(other, LocatorBase):
            return False
        return self.to_external_form() == other.to_external_form()

    def __ne__ (self, other):
        return not(self.__eq__(other))


class Locator (LocatorBase):

    def __init__ (self, reference):
        self.generate_forms(reference)

