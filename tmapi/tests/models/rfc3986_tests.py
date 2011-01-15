"""Module containing tests of the examples from RFC 3986 - 5.4.1
Normal Examples."""

from tmapi_test_case import TMAPITestCase


class RFC3986Test (TMAPITestCase):

    def test_rfc_3986_5_4_1_normal_examples (self):
        iris = (
            ('g:h', 'g:h'),
            ('g', 'http://a/b/c/g'),
            ('./g', 'http://a/b/c/g'),
            ('/g', 'http://a/g'),
            ('//g/x', 'http://g/x'),
            ('?y', 'http://a/b/c/d;p?y'),
            ('g?y', 'http://a/b/c/g?y'),
            ('#s', 'http://a/b/c/d;p?q#s'),
            ('g#s', 'http://a/b/c/g#s'),
            ('g?y#s', 'http://a/b/c/g?y#s'),
            (';x', 'http://a/b/c/;x'),
            ('g;x', 'http://a/b/c/g;x'),
            ('g;x?y#s', 'http://a/b/c/g;x?y#s'),
            ('', 'http://a/b/c/d;p?q'),
            ('.', 'http://a/b/c/'),
            ('./', 'http://a/b/c/'),
            ('..', 'http://a/b/'),
            ('../', 'http://a/b/'),
            ('../g', 'http://a/b/g'),
            ('../..', 'http://a/'),
            ('../../', 'http://a/'),
            ('../../g', 'http://a/g')
            )
        reference = 'http://a/b/c/d;p?q'
        base = self.tm.create_locator(reference)
        self.assertEqual(reference, base.to_external_form())
        for part, expected in iris:
            self.assertEqual(expected, base.resolve(part).to_external_form(),
                             'Unexpected IRI resolution for ' + part)
