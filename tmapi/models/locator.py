import unicodedata
import urllib
import urlparse


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

    def resolve (self, reference):
        """Resolves the `reference` against this locator.

        The returned `Locator` represents an absolute IRI.

        :param reference: the reference which should be resolved
          against this locator
        :type reference: string
        :rtype: `Locator`

        """
        return Locator(urlparse.urljoin(self._external, reference))
    
    def to_external_form (self):
        """Returns the external form of the IRI.

        Any special character will be escaped using the escaping
        conventions of RFC 3987.

        :rtype: String

        """
        return self._external

    def normalise (self, reference):
        parts = list(urlparse.urlsplit(reference))
        parts[2] = urllib.quote(parts[2], '/;')
        url = unicode(urlparse.urlunsplit(parts), 'utf-8', 'replace')
        return url
    
    def unnormalise (self, reference):
        if not isinstance(reference, unicode):
            reference = unicode(urllib.unquote(reference), 'utf-8', 'replace')
        else:
            reference = urllib.unquote(reference)
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

    def __unicode__ (self):
        return self._reference
