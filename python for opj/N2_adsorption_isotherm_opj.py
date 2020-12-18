# Python script for import of N2 adsorption isotherm to be used in opj files
import re
import math
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
		self.new_bet_surface_area_report_titles = []
		self.bet_surface_area_report = []
		self.bet_surface_area_report_units = []
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
		self.new_micropore_report_titles = []
		self.bjh_adsorption_report_titles = []
		self.bjh_adsorption_report = []
		self.bjh_desorption_report_titles = []
		self.bjh_desorption_report = []
		self.summary_report = []
		self.new_analysis_log_titles = []
		self.new_analysis_log = []
		self.analysis_log_units = []
		# self.df_analysis_log = pd.DataFrame()
		# self.df_bet = pd.DataFrame()
		# self.df_micropore = pd.DataFrame()
		# self.df_bjh_adsorption = pd.DataFrame()
		# self.df_bjh_desorption = pd.DataFrame()
		# self.summary_report_dict = {}
		if self.file_name:
			self.isotherm_read()
		
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
						self.sample_directory = line[start_name_search:end_name_search].split()[
							0]
						self.sample_number = line[start_name_search:end_name_search].split()[
							1]
						m_time = time_re.search(line[end_name_search:])
						m_date = date_re.search(line[end_name_search:])
						self.start_time = m_time.group()
						self.start_date = m_date.group()
					
					if m_sample_id:
						start_id_search = m_sample_id.end()
						m_compl = compl_re.search(line)
						end_id_search = m_compl.start() - 1
						self.sample_id = line[start_id_search:end_id_search].strip(
						)
						m_time = time_re.search(line[end_id_search:])
						m_date = date_re.search(line[end_id_search:])
						self.compl_time = m_time.group()
						self.compl_date = m_date.group()
						
					if m_submitter:
						start_submitter_search = m_submitter.end()
						m_reprt = reprt_re.search(line)
						end_submitter_search = m_reprt.start() - 1
						self.submitter = line[start_submitter_search:end_submitter_search].strip(
						)
						m_time = time_re.search(line[end_submitter_search:])
						m_date = date_re.search(line[end_submitter_search:])
						self.reprt_time = m_time.group()
						self.reprt_date = m_date.group()
						
					if m_operator:
						start_operator_search = m_operator.end()
						m_sample_wt = sample_wt_re.search(line)
						end_operator_search = m_sample_wt.start() - 1
						self.operator = line[start_operator_search:end_operator_search].strip(
						)
						self.sample_wt = line[m_sample_wt.end():].strip()
						
					if m_station_number:
						m_equil_interval = equil_interval_re.search(line)
						m_free_space = free_space_re.search(line)
						self.station_number = line[m_station_number.end(
						):m_equil_interval.start()-1].strip()
						self.equil_interval = line[m_equil_interval.end(
						):m_free_space.start()-1].strip()
						self.free_space = line[m_free_space.end():].strip()
						info_flag = True
						
				m_analysis_log = analysis_log_re.search(line)
				m_bet_surface_area_report = bet_surface_area_report_re.search(
					line)
				m_micropore_analysis_report = micropore_analysis_report_re.search(
					line)
					
				if analysis_log_flag:
					if line.strip():
						if micromeritics_re.search(line):
							analysis_log_flag = False
						if analysis_log_flag:
							if line.split()[0].isalpha():
								self.analysis_log_titles.append(
									list(filter(None, re.split(r'\s{2,}', line.strip()))))
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
						m_correlation_coefficient = correlation_coefficient_re.search(
							line)
							
						if m_bet_surface_area:
							self.bet_surface_area = line[m_bet_surface_area.end():].split()[
								0]
							self.bet_surface_area_deviation = line[m_bet_surface_area.end():].split()[
								2]
						if m_slope:
							self.bet_slope = line[m_slope.end():].split()[0]
							self.bet_slope_deviation = line[m_slope.end():].split()[
								2]
						if m_y_intercept:
							self.bet_y_intercept = line[m_y_intercept.end():].split()[
								0]
							self.bet_y_intercept_deviation = line[m_y_intercept.end():].split()[
								2]
						if m_c:
							self.c = line[m_c.end():].strip()
						if m_vm:
							self.vm = line[m_vm.end():].split()[0]
								
						if micromeritics_re.search(line):
							bet_surface_area_report_falg = False
							bet_surface_area_table_flag = False
							
						if bet_surface_area_table_flag:
							if line.split()[0].isalpha():
								self.bet_surface_area_report_titles.append(
									list(filter(None, re.split(r'\s{2,}', line.strip()))))
							else:
								self.bet_surface_area_report.append(
									line.split())
									
						if m_correlation_coefficient:
							self.correlation_coefficient_bet = line[m_correlation_coefficient.end(
							):].strip()
							bet_surface_area_table_flag = True
							
				if micropore_analysis_report_flag:
					if line.strip():
						m_micropore_volume = micropore_volume_re.search(line)
						m_micropore_area = micropore_area_re.search(line)
						m_external_surface_area = external_surface_area_re.search(
							line)
						m_slope = slope_re.search(line)
						m_y_intercept = y_intercept_re.search(line)
						m_correlation_coefficient = correlation_coefficient_re.search(
							line)
							
						if m_micropore_volume:
							self.micropore_volume = line[m_micropore_volume.end():].split()[
								0]
						if m_micropore_area:
							self.micropore_area = line[m_micropore_area.end():].split()[
								0]
						if m_external_surface_area:
							self.external_surface_area = line[m_external_surface_area.end():].split()[
								0]
						if m_slope:
							self.micropore_slope = line[m_slope.end():].split()[
								0]
							self.micropore_slope_deviation = line[m_slope.end():].split()[
								2]
						if m_y_intercept:
							self.micropore_y_intercept = line[m_y_intercept.end():].split()[
								0]
							self.micropore_y_intercept_deviation = line[m_y_intercept.end():].split()[
								2]
									
						if micropore_postscript_re.search(line):
							micropore_table_flag = False
							micropore_postscript_flag = True
							
						if micromeritics_re.search(line):
							micropore_postscript_flag = False
							
						if micropore_postscript_flag:
							self.micropore_postscript.append(line.strip())
							
						if micropore_table_flag:
							if line.split()[0].isalpha():
								self.micropore_report_titles.append(
									list(filter(None, re.split(r'\s{2,}', line.strip()))))
									
							else:
								self.micropore_report.append(line.split())
								
						if m_correlation_coefficient:
							self.correlation_coefficient_micropore = line[m_correlation_coefficient.end(
							):].strip()
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
							self.bjh_adsorption_report_titles.append(
								list(filter(None, re.split(r'\s{1,}', line.strip()))))
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
							self.bjh_desorption_report_titles.append(
								list(filter(None, re.split(r'\s{1,}', line.strip()))))
						else:
							self.bjh_desorption_report.append(line.split())
							
				if m_bjh_desorption:
					bjh_desorption_flag = True
					
				m_summary_report = summary_report_re.search(line)
				
				if summary_flag:
					if line.strip():
						self.summary_report.append(
							list(filter(None, re.split(r'\s{2,}', line.strip()))))
							
				if m_summary_report:
					summary_flag = True
					
			f.close()
		
		summary_report_new = [
							self.summary_report[1],
							self.summary_report[2],
							self.summary_report[3] + self.summary_report[4],
							self.summary_report[5] + self.summary_report[6],
							self.summary_report[7],
							self.summary_report[9] + self.summary_report[10],
							self.summary_report[11] + self.summary_report[12],
							self.summary_report[13] + self.summary_report[14],
							self.summary_report[15],
							self.summary_report[17],
							self.summary_report[18],
							self.summary_report[19]
								]
		self.summary_report_dict = {
							summary_report_new[0][0][:-1]: summary_report_new[0][1],
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
							
		# analysis log report
		self.new_analysis_log_titles = [' '.join(i) for i in zip(self.analysis_log_titles[0],
															self.analysis_log_titles[1])]
		self.analysis_log_units.append('')
		for i in range(1, len(self.new_analysis_log_titles)):
			units = re.search(r'\([\w\/\: ]*\)', self.new_analysis_log_titles[i])
			rest_title = ''.join(self.new_analysis_log_titles[i].split('(')[0].strip())
			self.analysis_log_units.append(units.group()[1:-1])
			self.new_analysis_log_titles[i] = rest_title
		
		for i in self.analysis_log:
			if len(i) == 2:
				if len(i[0].split(':')[0]) == 1:
					time_form = '000:0'+i[0]+':00.00'
				else:
					time_form = '000:'+i[0]+':00.00'
				self.new_analysis_log.append(
					[float('nan'), float('nan'), float('nan'), time_form, float(i[1])])
			else:
				if len(i[3].split(':')[0]) == 1:
					time_form = '000:0'+i[3]+':00.00'
				else:
					time_form = '000:'+i[3]+':00.00'
				self.new_analysis_log.append(
					[float(i[0]), float(i[1]), float(i[2]), time_form, float('nan')])
		self.new_analysis_log = list(map(list, zip(*self.new_analysis_log)))
		
		# bet report
		for i in zip(self.bet_surface_area_report_titles[0],
						self.bet_surface_area_report_titles[1]):
			if i[0] == '1/':
				self.new_bet_surface_area_report_titles.append(''.join(i))
			else:
				self.new_bet_surface_area_report_titles.append(' '.join(i))
		
		self.bet_surface_area_report_units.append('')
		units = re.search(r'\([\w\/\: ]*\)', self.new_bet_surface_area_report_titles[1])
		rest_title = ''.join(self.new_bet_surface_area_report_titles[1].split('(')[0].strip())
		self.bet_surface_area_report_units.append(units.group()[1:-1])
		self.new_bet_surface_area_report_titles[1] = rest_title
		self.bet_surface_area_report_units.append('')
		
		self.bet_surface_area_report = [[float(i) for i in j] for j in self.bet_surface_area_report]
		self.bet_surface_area_report = list(map(list, zip(*self.bet_surface_area_report)))
		
		# micropore report df
		for i in zip(self.micropore_report_titles[0],
					self.micropore_report_titles[1]):
			self.new_micropore_report_titles.append(' '.join(i))
			
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
		print('bet surface area\t', self.bet_surface_area,
		r'+\-', self.bet_surface_area_deviation)
		print('slope\t', self.bet_slope, r'+\-', self.bet_slope_deviation)
		print('y-intercept\t', self.bet_y_intercept,
		r'+\-', self.bet_y_intercept_deviation)
		print('c\t', self.c)
		print('vm\t', self.vm, 'cc/g STP')
		print('correlation coefficient', self.correlation_coefficient_bet)
		print('micropore volume\t', self.micropore_volume, 'cc/g')
		print('micropore area\t', self.micropore_area, 'sq. m/g')
		print('external surface area\t', self.external_surface_area, 'sq. m/g')
		print('micropore slope\t', self.micropore_slope,
		r'+\-', self.micropore_slope_deviation)
		print('micropore y-intercept\t', self.micropore_y_intercept,
		r'+\-', self.micropore_y_intercept_deviation)
		print('micropore correlation coefficient',
		self.correlation_coefficient_micropore)
		print('micropore postscript ' +
		' '.join([self.micropore_postscript[0], self.micropore_postscript[1]]))
		print('micropore equation ' +
		''.join([self.micropore_postscript[3], '**', self.micropore_postscript[2]]))
	
	def plot_pressure(self):
		# Create worksheet page named 'MyData' using template named 'Origin'.
		pgName = PyOrigin.CreatePage(PyOrigin.PGTYPE_WKS, "MyData", "Origin", 1)
		wp = PyOrigin.Pages(str(pgName)) # Get page
		wks = PyOrigin.ActiveLayer()     # Get sheet
		
		# Setup worksheet.
		wks.SetData(self.new_analysis_log, -1) # Put imported data into worksheet.
		wks.SetName(self.file_name) # Set sheet name to file name without path.
		
		# Set worksheet label rows.
		for i in range(len(self.new_analysis_log_titles)):
			wks.Columns(i).SetLongName(self.new_analysis_log_titles[i])
			wks.Columns(i).SetUnits(self.analysis_log_units[i])
			
		wks.Columns(3).SetFormat(2) # Set time format
		wks.Columns(0).SetType(0)
		wks.Columns(1).SetType(0)
		wks.Columns(2).SetType(0)
		wks.Columns(3).SetType(3)
		wks.Columns(4).SetType(0)
		
		# Create graph page named 'MyGraph' using template named 'Origin'.
		pgName = PyOrigin.CreatePage(PyOrigin.PGTYPE_GRAPH, "MyGraph", "Origin", 1)
		gp = PyOrigin.Pages(str(pgName))
		gp.LT_execute("layer1.x.opposite = 1;layer1.y.opposite = 1;")
		gl = gp.Layers(0)

		# Create data range and plot it into the graph layer.
		rng = PyOrigin.NewDataRange()  # Create data range.
		rng.Add('X', wks, 0, 3, -1, 3) # Add worksheet's 4th col as X.
		rng.Add('Y', wks, 0, 1, -1, 1) # Add worksheet's 2nd col as Y.
		rng.Add('Y', wks, 0, 4, -1, 4)
		dp = gl.AddPlot(rng, 202)      # Plot data range.

	def plot_isotherm(self):
		# Create worksheet page named 'MyData' using template named 'Origin'.
		pgName = PyOrigin.CreatePage(PyOrigin.PGTYPE_WKS, "MyData", "Origin", 1)
		wp = PyOrigin.Pages(str(pgName)) # Get page
		wks = PyOrigin.ActiveLayer()     # Get sheet
		
		# Setup worksheet.
		wks.SetData(self.new_analysis_log, -1) # Put imported data into worksheet.
		wks.SetName(self.file_name) # Set sheet name to file name without path.
		
		# Set worksheet label rows.
		for i in range(len(self.new_analysis_log_titles)):
			wks.Columns(i).SetLongName(self.new_analysis_log_titles[i])
			wks.Columns(i).SetUnits(self.analysis_log_units[i])
			
		wks.Columns(3).SetFormat(2) # Set time format
		wks.Columns(0).SetType(3)
		wks.Columns(1).SetType(0)
		wks.Columns(2).SetType(0)
		wks.Columns(3).SetType(3)
		wks.Columns(4).SetType(0)
		
		# Create graph page named 'MyGraph' using template named 'Origin'.
		pgName = PyOrigin.CreatePage(PyOrigin.PGTYPE_GRAPH, "MyGraph", "Origin", 1)
		gp = PyOrigin.Pages(str(pgName))
		gp.LT_execute("layer1.x.opposite = 1;layer1.y.opposite = 1;")
		gl = gp.Layers(0)

		# Create data range and plot it into the graph layer.
		rng = PyOrigin.NewDataRange()  # Create data range.
		rng.Add('X', wks, 0, 0, -1, 0) # Add worksheet's 4th col as X.
		rng.Add('Y', wks, 0, 2, -1, 2) # Add worksheet's 2nd col as Y.
		dp = gl.AddPlot(rng, 202)      # Plot data range.
		
	def plot_bet_vol(self):
		# Create worksheet page named 'MyData1' using template named 'Origin'.
		pgName = PyOrigin.CreatePage(PyOrigin.PGTYPE_WKS, "MyData1", "Origin", 1)
		wp = PyOrigin.Pages(str(pgName)) # Get page
		wks = PyOrigin.ActiveLayer()     # Get sheet
		
		# Setup worksheet.
		wks.SetData(self.bet_surface_area_report, -1) # Put imported data into worksheet.
		wks.SetName(self.file_name) # Set sheet name to file name without path.
		
		# Set worksheet label rows.
		for i in range(len(self.new_bet_surface_area_report_titles)):
			wks.Columns(i).SetLongName(self.new_bet_surface_area_report_titles[i])
			wks.Columns(i).SetUnits(self.bet_surface_area_report_units[i])
			
		wks.Columns(0).SetType(3)
		wks.Columns(1).SetType(0)
		wks.Columns(2).SetType(0)
		
		# Create graph page named 'MyGraph1' using template named 'Origin'.
		pgName = PyOrigin.CreatePage(PyOrigin.PGTYPE_GRAPH, "MyGraph1", "Origin", 1)
		gp = PyOrigin.Pages(str(pgName))
		gp.LT_execute("layer1.x.opposite = 1;layer1.y.opposite = 1;")
		gl = gp.Layers(0)
		
		# Create data range and plot it into the graph layer.
		rng = PyOrigin.NewDataRange()  # Create data range.
		rng.Add('X', wks, 0, 0, -1, 0) # Add worksheet's 1st col as X.
		rng.Add('Y', wks, 0, 1, -1, 1) # Add worksheet's 2nd col as Y.
		dp = gl.AddPlot(rng, 202)      # Plot data range.

	def plot_bet(self):
		# Create worksheet page named 'MyData2' using template named 'Origin'.
		pgName = PyOrigin.CreatePage(PyOrigin.PGTYPE_WKS, "MyData2", "Origin", 1)
		wp = PyOrigin.Pages(str(pgName)) # Get page
		wks = PyOrigin.ActiveLayer()     # Get sheet
		
		# Setup worksheet.
		wks.SetData(self.bet_surface_area_report, -1) # Put imported data into worksheet.
		wks.SetName(self.file_name) # Set sheet name to file name without path.
		
		# Set worksheet label rows.
		for i in range(len(self.new_bet_surface_area_report_titles)):
			wks.Columns(i).SetLongName(self.new_bet_surface_area_report_titles[i])
			wks.Columns(i).SetUnits(self.bet_surface_area_report_units[i])
			
		wks.Columns(0).SetType(3)
		wks.Columns(1).SetType(0)
		wks.Columns(2).SetType(0)
		
		# Create graph page named 'MyGraph2' using template named 'Origin'.
		pgName = PyOrigin.CreatePage(PyOrigin.PGTYPE_GRAPH, "MyGraph2", "Origin", 1)
		gp = PyOrigin.Pages(str(pgName))
		gp.LT_execute("layer1.x.opposite = 1;layer1.y.opposite = 1;")
		gl = gp.Layers(0)
		
		# Create data range and plot it into the graph layer.
		rng = PyOrigin.NewDataRange()  # Create data range.
		rng.Add('X', wks, 0, 0, -1, 0) # Add worksheet's 1st col as X.
		rng.Add('Y', wks, 0, 2, -1, 2) # Add worksheet's 2nd col as Y.
		dp = gl.AddPlot(rng, 202)      # Plot data range.
		
if __name__ == '__main__':
	a = Isotherm('DATA73_X-Al2O3.083')
	print(a.micropore_report)
	print(a.new_micropore_report_titles)