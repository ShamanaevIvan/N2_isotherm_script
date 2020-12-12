# Python script for import of N2 adsorption isotherm to be used in opj files
import re
import PyOrigin

class Isotherm:
    '''
    Reads and stores data from ASAP 2400 V3.07 report file
    '''

    def __init__(self, file_name=''):
        self.file_name = file_name
        self.sample_directory = ''
        self.sample_number = ''
        self.start_time = ''
        self.start_date = ''
        self.sample_id = ''
        self.compl_time = ''
        self.compl_date = ''
        self.submitter = ''
        self.reprt_time = ''
        self.reprt_date = ''
        self.operator = ''
        self.sample_wt = ''
        self.station_number = ''
        self.equil_interval = ''
        self.free_space = ''
        self.analysis_log = []
        self.analysis_log_titles = []
        self.bet_surface_area = ''
        self.bet_surface_area_deviation = ''
        self.bet_surface_area_report_titles = []
        self.bet_surface_area_report = []
        self.bet_slope = ''
        self.bet_slope_deviation = ''
        self.bet_y_intercept = ''
        self.bet_y_intercept_deviation = ''
        self.c = ''
        self.vm = ''
        self.correlation_coefficient_bet = ''
        self.micropore_volume = ''
        self.micropore_area = ''
        self.external_surface_area = ''
        self.micropore_slope = ''
        self.micropore_slope_deviation = ''
        self.micropore_y_intercept = ''
        self.micropore_y_intercept_deviation = ''
        self.correlation_coefficient_micropore = ''
        self.micropore_report_titles = []
        self.micropore_report = []
        self.micropore_postscript = []
        self.bjh_adsorption_report_titles = []
        self.bjh_adsorption_report = []
        self.bjh_desorption_report_titles = []
        self.bjh_desorption_report = []
        self.summary_report = []
        self.df_analysis_log = pd.DataFrame()
        self.df_bet = pd.DataFrame()
        self.df_micropore = pd.DataFrame()
        self.df_bjh_adsorption = pd.DataFrame()
        self.df_bjh_desorption = pd.DataFrame()
        self.summary_report_dict = {}

        # if self.file_name:
        #     self.isotherm_read()

        def isotherm_read(self):
            '''
            Reads data from ASAP 2400 V3.07 report file
            '''
            analysis_log_flag = False
            info_flag = False
            bet_surface_area_report_falg = False
            bet_surface_area_table_flag = False
            micropore_analysis_report_flag = False
            micropore_table_flag = False
            micropore_postscript_flag = False
            bjh_adsorption_flag = False
            bjh_desorption_flag = False
            summary_flag = False

            page_re = re.compile(r'PAGE\s+\d+')
            sample_dir_num_re = re.compile(r'SAMPLE DIRECTORY/NUMBER:')
            start_re = re.compile('START')
            time_re = re.compile(r'\d+:\d+:\d+')
            date_re = re.compile(r'\d+/\d+/\d+')
            sample_id_re = re.compile('SAMPLE ID:')
            compl_re = re.compile('COMPL')
            submitter_re = re.compile('SUBMITTER:')
            reprt_re = re.compile('REPRT')
            operator_re = re.compile('OPERATOR:')
            sample_wt_re = re.compile('SAMPLE WT:')
            station_number_re = re.compile('STATION NUMBER:')
            equil_interval_re = re.compile('EQUIL INTERVAL:')
            free_space_re = re.compile('FREE SPACE:')
            analysis_log_re = re.compile('ANALYSIS LOG')
            micromeritics_re = re.compile('Micromeritics Instrument Corporation')
            bet_surface_area_report_re = re.compile('BET SURFACE AREA REPORT')
            bet_surface_area_re = re.compile('BET SURFACE AREA:')
            slope_re = re.compile('SLOPE:')
            y_intercept_re = re.compile('Y-INTERCEPT:')
            c_re = re.compile('C:')
            vm_re = re.compile('VM:')
            correlation_coefficient_re = re.compile('CORRELATION COEFFICIENT:')
            micropore_analysis_report_re = re.compile('MICROPORE ANALYSIS REPORT')
            micropore_volume_re = re.compile('MICROPORE VOLUME:')
            micropore_area_re = re.compile('MICROPORE AREA:')
            external_surface_area_re = re.compile('EXTERNAL SURFACE AREA:')
            micropore_postscript_re = re.compile(
                'THICKNESS VALUES USED IN THE LEAST-SQUARES ANALYSIS')
            bjh_adsorption_re = re.compile(
                'BJH ADSORPTION PORE DISTRIBUTION REPORT')
            bjh_desorption_re = re.compile(
                'BJH DESORPTION PORE DISTRIBUTION REPORT')
            summary_report_re = re.compile('SUMMARY REPORT')

            # Get path and name of a data file in Origin's Samples folder.
            originPath = PyOrigin.GetPath(PyOrigin.PATHTYPE_SYSTEM)
            dataFileName = originPath + "\\Samples\\Curve Fitting\\Step01.dat"
            
if __name__ == '__main__':
    print('test')