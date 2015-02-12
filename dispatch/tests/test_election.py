from mock import patch, mock_open, MagicMock
import dispatch.election as election

class TestElection(object):
    @patch('dispatch.election.KazooClient', create=True)
    @patch('dispatch.state.ARGS', create=True)
    def test_start_election_one_master(self, mock_args, mock_kazoo):
        mock_args.zookeeper = 'foo'
        mock_kazoo_client = MagicMock()
        mock_kazoo.return_value = mock_kazoo_client
        mock_kazoo_client.create.return_value = 'n_0000000001'
        mock_kazoo_client.get_children.return_value = ['n_0000000001']
        m = election.MasterElection()
        self.called = False
        def callback():
            self.called = True
        m.start_election(callback)
        assert self.called

    @patch('dispatch.election.KazooClient', create=True)
    @patch('dispatch.state.ARGS', create=True)
    def test_start_election_not_me(self, mock_args, mock_kazoo):
        mock_args.zookeeper = 'foo'
        mock_kazoo_client = MagicMock()
        mock_kazoo.return_value = mock_kazoo_client
        mock_kazoo_client.create.return_value = 'n_0000000002'
        mock_kazoo_client.get_children.return_value = ['n_0000000002',
                                                       'n_0000000001', ]
        m = election.MasterElection()
        self.called = False
        def callback():
            self.called = True
        m.start_election(callback)
        assert not self.called
