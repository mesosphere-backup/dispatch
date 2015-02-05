from mock import patch, mock_open
import dispatch.state as state

class TestState(object):
    @patch('dispatch.state.open', create=True)
    @patch('os.path.exists', new=lambda x: True)
    @patch('dispatch.state.ARGS', create=True)
    def test_persisted_queue_two(self, mock_args, mock_open_queue):
        file_data = '[{"id":"one", "location": "bar", "port": 1234, '\
            '"resource": "baz", "running": true, ' \
            '"data": "somescript", "uris": ["http://foo/"]}, ' \
            '{"id":"two", "location": "bar", "port": 456, '\
            '"resource": "baz", "running": true, ' \
            '"data": "somescript", "uris": ["http://bar/"]}]'
        mock_open(mock=mock_open_queue, read_data=file_data)
        mock_args.queue_dir = 'foo'
        state.CURRENT = state.State()
        assert len(state.CURRENT.queue.queue) == 2

    @patch('dispatch.state.open', create=True)
    @patch('os.path.exists', new=lambda x: True)
    @patch('dispatch.state.ARGS', create=True)
    def test_persisted_queue_one(self, mock_args, mock_open_queue):
        file_data = '[{"id":"foo", "location": "bar", "port": 1234, '\
            '"resource": "baz", "running": true, ' \
            '"data": "somescript", "uris": ["http://foo/"]}]'
        mock_open(mock=mock_open_queue, read_data=file_data)
        mock_args.queue_dir = 'foo'
        state.CURRENT = state.State()
        assert len(state.CURRENT.queue.queue) == 1

    @patch('dispatch.state.open', create=True)
    @patch('os.path.exists', new=lambda x: True)
    @patch('dispatch.state.ARGS', create=True)
    def test_persisted_queue_zero(self, mock_args, mock_open_queue):
        file_data = '[]'
        mock_open(mock=mock_open_queue, read_data=file_data)
        mock_args.queue_dir = 'foo'

        state.CURRENT = state.State()
        assert len(state.CURRENT.queue.queue) == 0

    @patch('os.path.exists', new=lambda x: False)
    @patch('dispatch.state.ARGS', create=True)
    def test_persisted_queue_no_file(self, mock_args):
        mock_args.queue_dir = 'foo'
        state.CURRENT = state.State()
        assert len(state.CURRENT.queue.queue) == 0
