import unittest
import unittest.mock

from aiohttp import helpers
from aiohttp import multidict


class HelpersTests(unittest.TestCase):

    def test_parse_mimetype(self):
        self.assertEqual(
            helpers.parse_mimetype(''), ('', '', '', {}))

        self.assertEqual(
            helpers.parse_mimetype('*'), ('*', '*', '', {}))

        self.assertEqual(
            helpers.parse_mimetype('application/json'),
            ('application', 'json', '', {}))

        self.assertEqual(
            helpers.parse_mimetype('application/json;  charset=utf-8'),
            ('application', 'json', '', {'charset': 'utf-8'}))

        self.assertEqual(
            helpers.parse_mimetype('''application/json; charset=utf-8;'''),
            ('application', 'json', '', {'charset': 'utf-8'}))

        self.assertEqual(
            helpers.parse_mimetype('ApPlIcAtIoN/JSON;ChaRseT="UTF-8"'),
            ('application', 'json', '', {'charset': 'UTF-8'}))

        self.assertEqual(
            helpers.parse_mimetype('application/rss+xml'),
            ('application', 'rss', 'xml', {}))

        self.assertEqual(
            helpers.parse_mimetype('text/plain;base64'),
            ('text', 'plain', '', {'base64': ''}))

    def test_basic_auth(self):
        # missing password here
        self.assertRaises(
            ValueError, helpers.BasicAuth, None)
        self.assertRaises(
            ValueError, helpers.BasicAuth, 'nkim', None)

        auth = helpers.BasicAuth('nkim')
        self.assertEqual(auth.login, 'nkim')
        self.assertEqual(auth.password, '')

        auth = helpers.BasicAuth('nkim', 'pwd')
        self.assertEqual(auth.login, 'nkim')
        self.assertEqual(auth.password, 'pwd')
        self.assertEqual(auth.encode(), 'Basic bmtpbTpwd2Q=')


class SafeAtomsTests(unittest.TestCase):

    def test_get_non_existing(self):
        atoms = helpers.SafeAtoms(
            {}, multidict.MultiDict(), multidict.MultiDict())
        self.assertEqual(atoms['unknown'], '-')

    def test_get_lower(self):
        i_headers = multidict.MultiDict([('test', '123')])
        o_headers = multidict.MultiDict([('TEST', '123')])

        atoms = helpers.SafeAtoms({}, i_headers, o_headers)
        self.assertEqual(atoms['{test}i'], '123')
        self.assertEqual(atoms['{test}o'], '-')
        self.assertEqual(atoms['{TEST}o'], '123')
        self.assertEqual(atoms['{UNKNOWN}o'], '-')
        self.assertEqual(atoms['{UNKNOWN}'], '-')
