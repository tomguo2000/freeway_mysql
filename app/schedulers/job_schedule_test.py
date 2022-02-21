import time
from app.utils.timeUtils import Timeutils
import os
from app.utils.setLogger import logger

def job_schedule_test():

    from run import application

    with application.app_context():
        from app.database.models.settings import SettingModel

        all_settings = SettingModel.query.all()

        logger.info('schedule run.........')

        for setting in all_settings:

            setting.modification_date = time.time()
            setting.last_modification_username = 'schedule'+'@'+Timeutils.timeStamp2timeString(setting.modification_date) \
            + '@' + str(os.getpid()) + '_' + str(os.getppid())
            setting.save_to_db()

        logger.info('schedule end..........')
