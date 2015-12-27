import cleanup
import loader
import py.test


class TestCleanUp:

    def setup_class(self):
        self.orgs = cleanup.Organization()
        self.attorneys = cleanup.Attorney()

    def test_organizations(self):
        assert self.orgs.count == 275

    def test_orgs_length(self):
        assert len(self.orgs.orgs) == 275

    def test_orgs_unique_length(self):
        assert len(self.orgs.get_unique_orgs()) == 269

    def test_attorneys(self):
        assert self.attorneys.count == 4195

    def test_attorneys_length(self):
        assert len(self.attorneys.attorneys) == 4195


class TestLoader:

    def setup_class(self):
        self.loader = loader.Loader()

    def test_attorneys(self):
        assert len(self.loader.attorneys) == 4176

    def test_insert_attorneys(self):
        assert self.loader.insertAttorneys() == 4176
