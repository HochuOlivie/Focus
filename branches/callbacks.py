from .start.callbacks import register_callbacks as rc1
from .set.callbacks import register_callbacks as rc2
from .log.callbacks import register_callbacks as rc3
from .stat.callbacks import register_callbacks as rc4

callbacks = [rc1, rc2, rc3, rc4]
