import unittest
import pprint

from unittest import mock
from temporal_correlation import TemporalCorrelationAnalysis, GitCommit

# See https://dzone.com/articles/temporal-correlation-git
# http://michaelfeathers.typepad.com/michael_feathers_blog/2011/09/temporal-correlation-of-class-changes.html


class GitCommitTest(unittest.TestCase):

    @mock.patch('subprocess.Popen.communicate')
    def test_create_git_commit(self, mocked_instance):
        # Given.
        class StdOutMock(object):
            def splitlines(self):
                return ["file1.txt", "file2.txt"]

        git_commit = GitCommit(commit_id="abc")
        mocked_instance.return_value = (StdOutMock(), None)

        # When
        file_list = git_commit.read_files_belonging_to_commit()

        # Then
        self.assertEqual(['file1.txt', 'file2.txt'], file_list,
                         "Files list is present")

    def test_commit_score_score(self):
        # Given.
        git_commit = GitCommit(commit_id="abc")
        git_commit.__dict__["_entries"] = ["file1.txt", "file2.txt"]

        # When
        score = git_commit._commit_score()

        # Then
        self.assertEqual(0.5, score)

    def test_commit_score_oeps(self):
        # Given.
        git_commit = GitCommit(commit_id="abc")

        # When
        score = git_commit._commit_score()

        # Then
        self.assertEqual(0, score)

    def test_construct_key(self):
        # Given.
        git_commit = GitCommit(commit_id="abc")

        # When
        key = git_commit.construct_key("file_a", "file_b")

        # Then
        self.assertEqual("file_a -> file_b", key)


class TemporalCorrelationTest(unittest.TestCase):

    def setUp(self):
        self.analysis = TemporalCorrelationAnalysis()
        self.commit_ids = """bcce420a2d27558a5eb65ce5641cd978d86fb1f0
            2bd49b18e4af1a0ef134c81755b7a2cad2683c8e
            c85cda1f6ae899acb48b895adf8917ef7d5d4446"""

    def test_convert_to_git_commits(self):
        # When
        array = self.analysis.convert_to_git_commits(self.commit_ids)
        pprint.pprint(array)
        # Then
        expected = [
            GitCommit("bcce420a2d27558a5eb65ce5641cd978d86fb1f0"),
            GitCommit("2bd49b18e4af1a0ef134c81755b7a2cad2683c8e"),
            GitCommit("c85cda1f6ae899acb48b895adf8917ef7d5d4446")
        ]
        self.assertEqual(expected, array)

    def test_to_weighted_matrix(self):
        # Given
        git_commit1 = GitCommit(commit_id="abc")
        git_commit1.__dict__["_entries"] = ["file1.txt", "file2.txt"]

        git_commit2 = GitCommit(commit_id="abc")
        git_commit2.__dict__["_entries"] = ["file1.txt", "file2.txt"]

        git_commit3 = GitCommit(commit_id="abc")
        git_commit3.__dict__["_entries"] = ["file1.txt", "file2.txt"]

        git_commits = [
            git_commit1,
            git_commit2,
            git_commit3
        ]

        # When
        matrix = self.analysis._to_weighted_matrix(git_commits)

        # Then
        expected_matrix = {}

        self.assertEqual(expected_matrix, matrix)
    #
    # def test_print_top_10(self):
    #     # Given
    #     array = [
    #         ["gall/apps/cms/tests/test_views.py"],
    #         ["config/base.cfg", "setup.cfg"],
    #         ["config/a.log", "setup.cfg"],
    #         ["config/a.log", "setup.cfg"],
    #         ["config/a.log", "setup.cfg"]
    #     ]
    #
    #     # When
    #     result = self.analysis.print_top10(array)
    #     pprint.pprint(result)
    #
    #     # Then
    #     expected = [('setup.cfg -> setup.cfg', 2.0),
    #                 ('config/a.log -> setup.cfg', 1.5),
    #                 ('setup.cfg -> config/a.log', 1.5),
    #                 ('config/a.log -> config/a.log', 1.5),
    #                 ('gall/apps/cms/tests/test_views.py -> gall/apps/cms/tests/test_views.py',
    #                  1.0),
    #                 ('setup.cfg -> config/base.cfg', 0.5),
    #                 ('config/base.cfg -> setup.cfg', 0.5),
    #                 ('config/base.cfg -> config/base.cfg', 0.5)]
    #     self.assertSetEqual(expected, result, msg="The top most element")


if __name__ == '__main__':
    unittest.main()
