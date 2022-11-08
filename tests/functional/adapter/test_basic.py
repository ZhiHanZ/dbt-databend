import pytest

from dbt.tests.adapter.basic.test_base import BaseSimpleMaterializations
from dbt.tests.adapter.basic.test_singular_tests import BaseSingularTests
from dbt.tests.adapter.basic.test_singular_tests_ephemeral import (
    BaseSingularTestsEphemeral
)
from dbt.tests.adapter.basic.test_empty import BaseEmpty
from dbt.tests.adapter.basic.test_ephemeral import BaseEphemeral
from dbt.tests.adapter.basic.test_incremental import BaseIncremental
from dbt.tests.adapter.basic.test_generic_tests import BaseGenericTests
from dbt.tests.adapter.basic.test_snapshot_check_cols import BaseSnapshotCheckCols
from dbt.tests.adapter.basic.test_snapshot_timestamp import BaseSnapshotTimestamp
from dbt.tests.adapter.basic.test_adapter_methods import BaseAdapterMethod


class TestSimpleMaterializationsDatabend(BaseSimpleMaterializations):
    pass


class TestSingularTestsDatabend(BaseSingularTests):
    pass


class TestSingularTestsEphemeralDatabend(BaseSingularTestsEphemeral):
    pass


class TestEmptyDatabend(BaseEmpty):
    pass


# class TestEphemeralDatabend(BaseEphemeral):
#     pass


class TestIncrementalDatabend(BaseIncremental):
    pass


class TestGenericTestsDatabend(BaseGenericTests):
    pass


# class TestSnapshotCheckColsDatabend(BaseSnapshotCheckCols):
#     pass


# class TestSnapshotTimestampDatabend(BaseSnapshotTimestamp):
#     pass


class TestBaseAdapterMethodDatabend(BaseAdapterMethod):
    pass
