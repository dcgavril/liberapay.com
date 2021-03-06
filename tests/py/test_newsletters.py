from __future__ import absolute_import, division, print_function, unicode_literals

from liberapay.testing import Harness


class TestNewsletters(Harness):

    def setUp(self):
        Harness.setUp(self)
        self.alice = self.make_participant('alice')
        self.bob = self.make_participant('bob')

    def test_subscribe_and_unsubscribe(self):
        r = self.client.POST('/alice/subscribe', auth_as=self.bob, xhr=True)
        assert r.code == 200

        r = self.client.POST('/alice/unsubscribe', auth_as=self.bob, xhr=True)
        assert r.code == 200

    def test_subscribe_and_unsubscribe_as_anon(self):
        r = self.client.POST('/alice/subscribe', xhr=True, raise_immediately=False)
        assert r.code == 403

        r = self.client.POST('/alice/unsubscribe', xhr=True, raise_immediately=False)
        assert r.code == 403

    def test_unsubscribe_and_subscribe_with_token(self):
        subscription = self.bob.upsert_subscription(True, self.alice.id)
        assert self.alice.check_subscription_status(self.bob) is True
        unsubscribe_url = '/~{publisher}/unsubscribe?id={id}&token={token}'.format(**subscription._asdict())

        r = self.client.POST(unsubscribe_url, xhr=True)
        assert r.code == 200
        assert self.alice.check_subscription_status(self.bob) is False

        subscribe_url = unsubscribe_url.replace('/unsubscribe', '/subscribe')
        r = self.client.POST(subscribe_url, xhr=True)
        assert r.code == 200
