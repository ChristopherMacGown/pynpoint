import unittest
from pynpoint import redis
from pynpoint.config import Config

class RedisTestCase(unittest.TestCase):
    def setUp(self):
        # Clear out the shared state
        self.config = Config()
        self.config._clear()

        self.config = Config(config_files=["tests/data/redis.cfg"])
        self.redis = redis.Redis(config=self.config)

    def tearDown(self):
        self.redis.flushdb()

    def test_proper_assimilation(self):
        local_redis = redis.Redis(config=self.config)
        self.assertEqual(local_redis.conn, self.redis.conn)
        self.assertNotEqual(local_redis, self.redis)

    def test_push_to_a_list(self):
        self.assertTrue(self.redis.lpush('list', 1))
        self.assertTrue(self.redis.lpush('list', 2))
        self.assertTrue(self.redis.lpush('list', 3))
        self.assertEqual(self.redis.llen('list'), 3)

    def test_pop_from_a_list(self):
        self.redis.lpush('list', 2)
        self.redis.lpush('list', 2)
        self.redis.lpush('list', 3)
        self.assertTrue(self.redis.lpop('list'))
        self.assertTrue(self.redis.lpop('list'))
        self.assertTrue(self.redis.lpop('list'))
        self.assertFalse(self.redis.lpop('list'))
