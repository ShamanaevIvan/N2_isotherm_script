import re
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class Isotherm:
    def __init__(self, file_name=''):
        self.file_name                         = file_name
        self.sample_directory                  = ''
        self.sample_number                     = ''
        self.start_time                        = ''
        self.start_date                        = ''
        self.sample_id                         = ''
        self.compl_time                        = ''
        self.compl_date                        = ''
        self.submitter                         = ''
        self.reprt_time                        = ''
        self.reprt_date                        = ''
        self.operator                          = ''
        self.sample_wt                         = ''
        self.station_number                    = ''
        self.equil_interval                    = ''
        self.free_space                        = ''
        self.analysis_log                      = []
        self.analysis_log_titles               = []
        self.bet_surface_area                  = ''
        self.bet_surface_area_deviation        = ''
        self.bet_surface_area_report_titles    = []
        self.bet_surface_area_report           = []
        self.bet_slope                         = ''
        self.bet_slope_deviation               = ''
        self.bet_y_intercept                   = ''
        self.bet_y_intercept_deviation         = ''
        self.c                                 = ''
        self.vm                                = ''
        self.correlation_coefficient_bet       = ''
        self.micropore_volume                  = ''
        self.micropore_area                    = ''
        self.external_surface_area             = ''
        self.micropore_slope                   = ''
        self.micropore_slope_deviation         = ''
        self.micropore_y_intercept             = ''
        self.micropore_y_intercept_deviation   = ''
        self.correlation_coefficient_micropore = ''
        self.micropore_report_titles           = []
        self.micropore_report                  = []
        self.micropore_postscript              = []
        self.bjh_adsorption_report_titles      = []
        self.bjh_adsorption_report             = []
        self.bjh_desorption_report_titles      = []
        self.bjh_desorption_report             = []
        self.summary_report                    = []
        self.df_analysis_log                   = pd.DataFrame()
        self.df_bet                            = pd.DataFrame()
        self.df_micropore                      = pd.DataFrame()
        self.df_bjh_adsorption                 = pd.DataFrame()
        self.df_bjh_desorption                 = pd.DataFrame()
        self.summary_report_dict               = {}

        self.isotherm_read()
        
    def __str__(self):
        return 'file at {0}'.format(self.file_name)
    
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
        micropore_postscript_re = re.compile('THICKNESS VALUES USED IN THE LEAST-SQUARES ANALYSIS')
        bjh_adsorption_re = re.compile('BJH ADSORPTION PORE DISTRIBUTION REPORT')
        bjh_desorption_re = re.compile('BJH DESORPTION PORE DISTRIBUTION REPORT')
        summary_report_re = re.compile('SUMMARY REPORT')
        
        with open(self.file_name) as f:

            for line in f:

                if not info_flag:
                    m_sample_dir_num = sample_dir_num_re.search(line)
                    m_sample_id = sample_id_re.search(line)
                    m_submitter = submitter_re.search(line)
                    m_operator = operator_re.search(line)
                    m_station_number = station_number_re.search(line)

                    if m_sample_dir_num:
                        start_name_search = m_sample_dir_num.end()
                        m_start = start_re.search(line)
                        end_name_search = m_start.start() - 1
                        self.sample_directory = line[start_name_search:end_name_search].split()[0]
                        self.sample_number = line[start_name_search:end_name_search].split()[1]
                        m_time = time_re.search(line[end_name_search:])
                        m_date = date_re.search(line[end_name_search:])
                        self.start_time = m_time.group()
                        self.start_date = m_date.group()

                    if m_sample_id:
                        start_id_search = m_sample_id.end()
                        m_compl = compl_re.search(line)
                        end_id_search = m_compl.start() - 1
                        self.sample_id = line[start_id_search:end_id_search].strip()
                        m_time = time_re.search(line[end_id_search:])
                        m_date = date_re.search(line[end_id_search:])
                        self.compl_time = m_time.group()
                        self.compl_date = m_date.group()

                    if m_submitter:
                        start_submitter_search = m_submitter.end()
                        m_reprt = reprt_re.search(line)
                        end_submitter_search = m_reprt.start() - 1
                        self.submitter = line[start_submitter_search:end_submitter_search].strip()
                        m_time = time_re.search(line[end_submitter_search:])
                        m_date = date_re.search(line[end_submitter_search:])
                        self.reprt_time = m_time.group()
                        self.reprt_date = m_date.group()

                    if m_operator:
                        start_operator_search = m_operator.end()
                        m_sample_wt = sample_wt_re.search(line)
                        end_operator_search = m_sample_wt.start() - 1
                        self.operator = line[start_operator_search:end_operator_search].strip()
                        self.sample_wt = line[m_sample_wt.end():].strip()

                    if m_station_number:
                        m_equil_interval = equil_interval_re.search(line)
                        m_free_space = free_space_re.search(line)
                        self.station_number = line[m_station_number.end():m_equil_interval.start()-1].strip()
                        self.equil_interval = line[m_equil_interval.end():m_free_space.start()-1].strip()
                        self.free_space = line[m_free_space.end():].strip()
                        info_flag = True

                m_analysis_log = analysis_log_re.search(line)
                m_page = page_re.search(line)
                m_bet_surface_area_report = bet_surface_area_report_re.search(line)
                m_micropore_analysis_report = micropore_analysis_report_re.search(line)

                if m_page:
                    page_number = m_page.group().split()[-1]

                if analysis_log_flag:
                    if line.strip():
                        if micromeritics_re.search(line):
                            analysis_log_flag = False
                        if analysis_log_flag:
                            if line.split()[0].isalpha():
                                self.analysis_log_titles.append(list(filter(None, re.split(r'\s{2,}', line.strip()))))
                            else:
                                self.analysis_log.append(line.split())

                if m_analysis_log:
                    analysis_log_flag = True

                if bet_surface_area_report_falg:
                    if line.strip():
                        m_bet_surface_area = bet_surface_area_re.search(line)
                        m_slope = slope_re.search(line)
                        m_y_intercept = y_intercept_re.search(line)
                        m_c = c_re.search(line)
                        m_vm = vm_re.search(line)
                        m_correlation_coefficient= correlation_coefficient_re.search(line)

                        if m_bet_surface_area:
                            self.bet_surface_area = line[m_bet_surface_area.end():].split()[0]
                            self.bet_surface_area_deviation = line[m_bet_surface_area.end():].split()[2]
                        if m_slope:
                            self.bet_slope = line[m_slope.end():].split()[0]
                            self.bet_slope_deviation = line[m_slope.end():].split()[2]
                        if m_y_intercept:
                            self.bet_y_intercept = line[m_y_intercept.end():].split()[0]
                            self.bet_y_intercept_deviation = line[m_y_intercept.end():].split()[2]
                        if m_c:
                            self.c = line[m_c.end():].strip()
                        if m_vm:
                            self.vm = line[m_vm.end():].split()[0]

                        if micromeritics_re.search(line):
                            bet_surface_area_report_falg = False
                            bet_surface_area_table_flag = False

                        if bet_surface_area_table_flag:
                            if line.split()[0].isalpha():
                                self.bet_surface_area_report_titles.append(list(filter(None, re.split(r'\s{2,}', line.strip()))))
                            else:
                                self.bet_surface_area_report.append(line.split())

                        if m_correlation_coefficient:
                            self.correlation_coefficient_bet = line[m_correlation_coefficient.end():].strip()
                            bet_surface_area_table_flag = True

                if micropore_analysis_report_flag:
                    if line.strip():
                        m_micropore_volume = micropore_volume_re.search(line)
                        m_micropore_area = micropore_area_re.search(line)
                        m_external_surface_area = external_surface_area_re.search(line)
                        m_slope = slope_re.search(line)
                        m_y_intercept = y_intercept_re.search(line)
                        m_correlation_coefficient= correlation_coefficient_re.search(line)

                        if m_micropore_volume:
                            self.micropore_volume = line[m_micropore_volume.end():].split()[0]
                        if m_micropore_area:
                            self.micropore_area = line[m_micropore_area.end():].split()[0]
                        if m_external_surface_area:
                            self.external_surface_area = line[m_external_surface_area.end():].split()[0]
                        if m_slope:
                            self.micropore_slope = line[m_slope.end():].split()[0]
                            self.micropore_slope_deviation = line[m_slope.end():].split()[2]
                        if m_y_intercept:
                            self.micropore_y_intercept = line[m_y_intercept.end():].split()[0]
                            self.micropore_y_intercept_deviation = line[m_y_intercept.end():].split()[2]

                        if micropore_postscript_re.search(line):
                            micropore_table_flag = False
                            micropore_postscript_flag = True

                        if micromeritics_re.search(line):
                            micropore_postscript_flag = False

                        if micropore_postscript_flag:
                            self.micropore_postscript.append(line.strip())

                        if micropore_table_flag:
                            if line.split()[0].isalpha():
                                self.micropore_report_titles.append(list(filter(None, re.split(r'\s{2,}', line.strip()))))
                            else:
                                self.micropore_report.append(line.split())

                        if m_correlation_coefficient:
                            self.correlation_coefficient_micropore = line[m_correlation_coefficient.end():].strip()
                            micropore_table_flag = True

                if m_bet_surface_area_report:
                    bet_surface_area_report_falg = True

                if m_micropore_analysis_report:
                    micropore_analysis_report_flag = True

                m_bjh_adsorption = bjh_adsorption_re.search(line)

                if micromeritics_re.search(line):
                    bjh_adsorption_flag = False

                if bjh_adsorption_flag:
                    if line.strip():
                        if line.split()[0].isalpha() or (line.split()[0][0] == '('):
                            self.bjh_adsorption_report_titles.append(list(filter(None, re.split(r'\s{1,}', line.strip()))))
                        else:
                            self.bjh_adsorption_report.append(line.split())

                if m_bjh_adsorption:
                    bjh_adsorption_flag = True

                m_bjh_desorption = bjh_desorption_re.search(line)

                if micromeritics_re.search(line):
                    bjh_desorption_flag = False

                if bjh_desorption_flag:
                    if line.strip():
                        if line.split()[0].isalpha() or (line.split()[0][0] == '('):
                            self.bjh_desorption_report_titles.append(list(filter(None, re.split(r'\s{1,}', line.strip()))))
                        else:
                            self.bjh_desorption_report.append(line.split())

                if m_bjh_desorption:
                    bjh_desorption_flag = True    

                m_summary_report = summary_report_re.search(line)

                if summary_flag:
                    if line.strip():
                        self.summary_report.append(list(filter(None, re.split(r'\s{2,}', line.strip()))))

                if m_summary_report:
                    summary_flag = True

            f.close()
       
        summary_report_new = [self.summary_report[1],
                              self.summary_report[2],
                              self.summary_report[3]+self.summary_report[4],
                              self.summary_report[5]+self.summary_report[6],
                              self.summary_report[7],
                              self.summary_report[9]+self.summary_report[10],
                              self.summary_report[11]+self.summary_report[12],
                              self.summary_report[13]+self.summary_report[14],
                              self.summary_report[15],
                              self.summary_report[17],
                              self.summary_report[18],
                              self.summary_report[19]]
        self.summary_report_dict = {summary_report_new[0][0][:-1]: summary_report_new[0][1],
                                    summary_report_new[1][0][:-1]: summary_report_new[1][1],
                                    ' '.join(summary_report_new[2][:5])[:-1]: summary_report_new[2][5],
                                    ' '.join(summary_report_new[3][:5])[:-1]: summary_report_new[3][5],
                                    summary_report_new[4][0][:-1]: summary_report_new[4][1],
                                    ' '.join(summary_report_new[5][:3])[:-1]: summary_report_new[5][3].split()[0],
                                    ' '.join(summary_report_new[6][:5])[:-1]: summary_report_new[6][5].split()[0],
                                    ' '.join(summary_report_new[7][:5])[:-1]: summary_report_new[7][5].split()[0],
                                    summary_report_new[8][0][:-1]: summary_report_new[8][1].split()[0],
                                    summary_report_new[9][0][:-1]: summary_report_new[9][1],
                                    summary_report_new[10][0][:-1]: summary_report_new[10][1],
                                    summary_report_new[11][0][:-1]: summary_report_new[11][1],
                                    }

        # analysis log report df
        new_analysis_log_titles = [' '.join(i) for i in zip(self.analysis_log_titles[0],
                                                            self.analysis_log_titles[1])]
        new_analysis_log = []
        for i in self.analysis_log:
            if len(i) == 2:
                new_analysis_log.append([np.NaN, np.NaN, np.NaN, i[0], float(i[1])])
            else:
                new_analysis_log.append([float(i[0]), float(i[1]), float(i[2]), i[3], np.NaN])

        self.df_analysis_log = pd.DataFrame(new_analysis_log, columns=new_analysis_log_titles)
        log_timedelta_series = pd.to_timedelta('0' + self.df_analysis_log['ELAPSED TIME (HR:MN)'] + ':00')
        self.df_analysis_log['ELAPSED TIME (HR:MN)'] = log_timedelta_series
        self.df_analysis_log['DATE'] = pd.to_datetime(' '.join([self.start_date,
                                                                self.start_time])) + log_timedelta_series
        self.df_analysis_log.set_index('DATE', inplace=True)

        # bet report df
        new_bet_surface_area_report_titles = []
        for i in zip(self.bet_surface_area_report_titles[0],
                     self.bet_surface_area_report_titles[1]):
            if i[0] == '1/':
                new_bet_surface_area_report_titles.append(''.join(i))
            else:
                new_bet_surface_area_report_titles.append(' '.join(i))

        self.df_bet = pd.DataFrame(self.bet_surface_area_report, columns=new_bet_surface_area_report_titles)

        # micropore report df
        new_micropore_report_titles = []
        for i in zip(self.micropore_report_titles[0],
                     self.micropore_report_titles[1]):
                new_micropore_report_titles.append(' '.join(i))

        self.df_micropore = pd.DataFrame(self.micropore_report,
                                         columns=new_micropore_report_titles)

        # bjh adsorption report df
        new_bjh_adsorption_report_titles = []
        new_bjh_adsorption_report_titles.append([' '.join([self.bjh_adsorption_report_titles[0][0],
                                                           self.bjh_adsorption_report_titles[0][1]]),
                                                 self.bjh_adsorption_report_titles[0][2],
                                                 self.bjh_adsorption_report_titles[0][3],
                                                 self.bjh_adsorption_report_titles[0][4],
                                                 self.bjh_adsorption_report_titles[0][5],
                                                 self.bjh_adsorption_report_titles[0][6]])
        new_bjh_adsorption_report_titles.append([self.bjh_adsorption_report_titles[1][0],
                                                 self.bjh_adsorption_report_titles[1][1],
                                                 ' '.join([self.bjh_adsorption_report_titles[1][2],
                                                           self.bjh_adsorption_report_titles[1][3]]),
                                                 ' '.join([self.bjh_adsorption_report_titles[1][4],
                                                           self.bjh_adsorption_report_titles[1][5]]),
                                                 ' '.join([self.bjh_adsorption_report_titles[1][6],
                                                           self.bjh_adsorption_report_titles[1][7]]),
                                                 ' '.join([self.bjh_adsorption_report_titles[1][8],
                                                           self.bjh_adsorption_report_titles[1][9]])])
        new_bjh_adsorption_report_titles.append([''.join([self.bjh_adsorption_report_titles[2][0],
                                                          self.bjh_adsorption_report_titles[2][1]]),
                                                 ''.join([self.bjh_adsorption_report_titles[2][2],
                                                          self.bjh_adsorption_report_titles[2][3]]),
                                                 self.bjh_adsorption_report_titles[2][4],
                                                 self.bjh_adsorption_report_titles[2][5],
                                                 ' '.join([self.bjh_adsorption_report_titles[2][6],
                                                          self.bjh_adsorption_report_titles[2][7]]),
                                                 ' '.join([self.bjh_adsorption_report_titles[2][8],
                                                          self.bjh_adsorption_report_titles[2][9]])])

        combined_bjh_adsorption_report_titles = [' '.join(i) for i in zip(new_bjh_adsorption_report_titles[0],
                                  new_bjh_adsorption_report_titles[1],
                                  new_bjh_adsorption_report_titles[2])]

        final_bjh_adsorption_report_titles = [combined_bjh_adsorption_report_titles[0]+' high',
                                              combined_bjh_adsorption_report_titles[0]+' low'] + \
                                                combined_bjh_adsorption_report_titles[1:]

        final_bjh_adsorption_report = [[i[0][:-1]]+i[1:] for i in self.bjh_adsorption_report]

        self.df_bjh_adsorption = pd.DataFrame(final_bjh_adsorption_report, columns=final_bjh_adsorption_report_titles)
        
        # bjh desorption report df
        new_bjh_desorption_report_titles = []
        new_bjh_desorption_report_titles.append([' '.join([self.bjh_desorption_report_titles[0][0],
                                                           self.bjh_desorption_report_titles[0][1]]),
                                                 self.bjh_desorption_report_titles[0][2],
                                                 self.bjh_desorption_report_titles[0][3],
                                                 self.bjh_desorption_report_titles[0][4],
                                                 self.bjh_desorption_report_titles[0][5],
                                                 self.bjh_desorption_report_titles[0][6]])
        new_bjh_desorption_report_titles.append([self.bjh_desorption_report_titles[1][0],
                                                 self.bjh_desorption_report_titles[1][1],
                                                 ' '.join([self.bjh_desorption_report_titles[1][2],
                                                           self.bjh_desorption_report_titles[1][3]]),
                                                 ' '.join([self.bjh_desorption_report_titles[1][4],
                                                           self.bjh_desorption_report_titles[1][5]]),
                                                 ' '.join([self.bjh_desorption_report_titles[1][6],
                                                           self.bjh_desorption_report_titles[1][7]]),
                                                 ' '.join([self.bjh_desorption_report_titles[1][8],
                                                           self.bjh_desorption_report_titles[1][9]])])
        new_bjh_desorption_report_titles.append([''.join([self.bjh_desorption_report_titles[2][0],
                                                          self.bjh_desorption_report_titles[2][1]]),
                                                 ''.join([self.bjh_desorption_report_titles[2][2],
                                                          self.bjh_desorption_report_titles[2][3]]),
                                                 self.bjh_desorption_report_titles[2][4],
                                                 self.bjh_desorption_report_titles[2][5],
                                                 ' '.join([self.bjh_desorption_report_titles[2][6],
                                                          self.bjh_desorption_report_titles[2][7]]),
                                                 ' '.join([self.bjh_desorption_report_titles[2][8],
                                                          self.bjh_desorption_report_titles[2][9]])])

        combined_bjh_desorption_report_titles = [' '.join(i) for i in zip(new_bjh_desorption_report_titles[0],
                                  new_bjh_desorption_report_titles[1],
                                  new_bjh_desorption_report_titles[2])]

        final_bjh_desorption_report_titles = [combined_bjh_desorption_report_titles[0]+' high',
                                              combined_bjh_desorption_report_titles[0]+' low'] + \
                                                combined_bjh_desorption_report_titles[1:]

        final_bjh_desorption_report = [[i[0][:-1]]+i[1:] for i in self.bjh_desorption_report]

        self.df_bjh_desorption = pd.DataFrame(final_bjh_desorption_report, columns=final_bjh_desorption_report_titles)
        return self.df_bjh_desorption

    def print_info(self):
        print('sample directory\t', self.sample_directory)
        print('sample number\t', self.sample_number)
        print('start_time\t', self.start_time)
        print('start_date\t', self.start_date)
        print('sample id\t', self.sample_id)
        print('compl time\t', self.compl_time)
        print('compl date\t', self.compl_date)
        print('submitter\t', self.submitter)
        print('reprt time\t', self.reprt_time)
        print('reprt date\t', self.reprt_date)
        print('operator\t', self.operator)
        print('sample wt\t', self.sample_wt)
        print('station number\t', self.station_number)
        print('equil interal\t', self.equil_interval)
        print('free space\t', self.free_space)
        print('bet surface area\t', self.bet_surface_area, r'+\-', self.bet_surface_area_deviation)
        print('slope\t', self.bet_slope, r'+\-', self.bet_slope_deviation)
        print('y-intercept\t', self.bet_y_intercept, r'+\-', self.bet_y_intercept_deviation)
        print('c\t', self.c)
        print('vm\t', self.vm, 'cc/g STP')
        print('correlation coefficient', self.correlation_coefficient_bet)
        print('micropore volume\t', self.micropore_volume, 'cc/g')
        print('micropore area\t', self.micropore_area, 'sq. m/g')
        print('external surface area\t', self.external_surface_area, 'sq. m/g')
        print('micropore slope\t', self.micropore_slope, r'+\-', self.micropore_slope_deviation)
        print('micropore y-intercept\t', self.micropore_y_intercept, r'+\-', self.micropore_y_intercept_deviation)
        print('micropore correlation coefficient', self.correlation_coefficient_micropore)
        print('micropore postscript ' + ' '.join([self.micropore_postscript[0], self.micropore_postscript[1]]))
        print('micropore equation ' + ''.join([self.micropore_postscript[3], '**', self.micropore_postscript[2]]))

    def plot_analysis_log(self):
        plt.plot(self.df_analysis_log['ELAPSED TIME (HR:MN)'].dt.seconds/3600,
                 self.df_analysis_log['PRESSURE (mmHg)'],
                 marker='o',
                 label='PRESSURE (mmHg)')
        plt.plot(self.df_analysis_log['ELAPSED TIME (HR:MN)'].dt.seconds/3600,
                 self.df_analysis_log['SATURATION PRESS.(mmHg)'],
                 marker='o',
                 label='SATURATION PRESS.(mmHg)')
        plt.legend()

    def plot_isotherm(self):
        plt.plot(self.df_analysis_log['RELATIVE PRESSURE'].values[~np.isnan(self.df_analysis_log['RELATIVE PRESSURE'].values)],
                 self.df_analysis_log['VOL ADSORBED (cc/g STP)'].values[~np.isnan(self.df_analysis_log['VOL ADSORBED (cc/g STP)'].values)])
        plt.xlabel('RELATIVE PRESSURE')
        plt.ylabel('VOL ADSORBED (cc/g STP)')

    def bet_plot1(self):
        plt.plot(self.df_bet['RELATIVE PRESSURE'].astype('float64'),
                 self.df_bet['VOL ADSORBED (cc/g STP)'].astype('float64'),
                 marker='o')
        plt.xlabel('RELATIVE PRESSURE')
        plt.ylabel('VOL ADSORBED (cc/g STP)')

    def bet_plot2(self):
        plt.plot(self.df_bet['RELATIVE PRESSURE'].astype('float64'),
                 self.df_bet['1/[VA(Po/P - 1)]'].astype('float64'),
                 marker='o')
        plt.xlabel('RELATIVE PRESSURE')
        plt.ylabel('1/[VA(Po/P - 1)]')

    def print_micropore_report(self):

        return self.df_micropore

    def micropore_plot(self):
        plt.plot(self.df_micropore['RELATIVE PRESSURE'].astype('float64'),
                 self.df_micropore['STATISTICAL THICKNESS,(A )'].astype('float64'),
                 marker='o')
        plt.xlabel('RELATIVE PRESSURE')
        plt.ylabel('STATISTICAL THICKNESS,(A )')

    def bjh_adsorption_plot(self):
        plt.plot(self.df_bjh_adsorption['AVERAGE DIAMETER (A)'].astype('float64'),
                 self.df_bjh_adsorption['INCREMENTAL PORE VOLUME (cc/g)'].astype('float64'),
                 marker='o'
                 )

    def bjh_desorption_plot(self):
        plt.plot(self.df_bjh_desorption['AVERAGE DIAMETER (A)'].astype('float64'),
                 self.df_bjh_desorption['INCREMENTAL PORE VOLUME (cc/g)'].astype('float64'),
                 marker='o'
                 )