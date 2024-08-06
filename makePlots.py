import math
import matplotlib.pyplot as plt
import numpy as np 
import csv 
  
#tools
def getTitle(var):

	titdic = {
		'Q2':r'$Q^2$ [GeV$^2$]',
		'xB':r'$x_{B}$',
		'Z':'$z$',
		'M_x':'$M_{X}$ [GeV$^2$]',
		'omega':r'$\omega$',
		'W2':r'$W^2$',
		'y':r'$y$',
		'p_e':r'$|p_{e}|$ [GeV]',
		'p_{\pi}':r'$|p_{\pi}|$ [GeV]',
		'w-':r'$w^-$',
		'w+':r'$w^+$',
		'w+/w-':r'$w^+/w^-$',
		}
	return titdic[var]

def divide_lists(list1, list2):
    if not list1 or not list2:
        return []
    return [list1[0] / list2[0]] + divide_lists(list1[1:], list2[1:])

def prop_err(list1, list2, list3, list4):
    if not list1 or not list2 or not list3 or not list4:
        return []
    return [list1[0]/list2[0]*math.sqrt( ( list3[0]/list1[0] )**2 + ( list4[0]/list2[0] )**2 )] + prop_err(list1[1:], list2[1:], list3 [1:], list4[1:] )

def ff(z):
	return (1-z)/(z+1)
	
#######################################
######################################
####################################


def makePlot( var, file1 ):
	with open( file1 ,'r') as csvfile: 
		plots1 = csv.reader(csvfile, delimiter = '\t') 
		x1 = []
		y1 = []
		unc = []

		for row in plots1: 
        
			x1.append(float(row[0])) 
			y1.append(float(row[1])) 
			unc.append(float(row[2])) 

	max_y1 = float(max(y1))

	plt.plot(x1, y1, 'ro') 
	plt.errorbar(x1, y1, yerr=unc, fmt='o')
	ax = plt.gca()
	ax.set_ylim([0, max_y1*1.2])
	plt.xlabel(getTitle(var)) 
	plt.ylabel('Counts [a.u.]') 
	plt.show() 

def makeComparison( var, fileList , titList, outFileName):
	colorList = ['red', 'blue', 'magenta', 'green', 'gold', 'cyan', 'black', 'blueviolet','darkorange', 'brown']

	xList = []
	yList = []	
	uncList = []

	for file in fileList:
		with open( file + '.csv' ,'r') as csvfile: 
			plots = csv.reader(csvfile, delimiter = '\t') 
			x1 = []
			y1 = []
			unc = []

			for row in plots: 
        
				x1.append(float(row[0])) 
				y1.append(float(row[1]))
				unc.append(float(row[2]))

			xList.append(x1)
			yList.append(y1) 
			uncList.append(unc)
	yMax = 0
	for yDat in yList:
		if max(yDat) > yMax:
			yMax = max(yDat)



	for i in range ( len ( yList ) ):
		yList[i] = np.where( yList[i]==0, np.nan, yList[i] )
		plt.plot( xList[i], yList[i], colorList[i], label = titList[i] )
		plt.errorbar(xList[i], yList[i], yerr=uncList[i], fmt='o')


	ax = plt.gca()
	ax.set_ylim( [0, yMax*1.2] )
	plt.xlabel( getTitle(var) )
	plt.ylabel('Counts [a.u.]')
	plt.legend()
	plt.savefig(outFileName+'.csv', bbox_inches='tight')

def makeRatioBinned( fileList , titList, outFileName):
	colorList = ['red', 'blue', 'magenta', 'green', 'gold', 'cyan', 'black', 'blueviolet','darkorange', 'brown']

	xList = []
	yList = []	
	uncList = []

	for file in fileList:
		with open( file ,'r') as csvfile: 
			plots = csv.reader(csvfile, delimiter = '\t') 
			x1 = []
			y1 = []
			unc = []

			for row in plots: 
        
				x1.append(float(row[0])) 
				y1.append(float(row[1]))
				unc.append(float(row[2]))
			print(x1)	

			xList.append(x1)
			yList.append(y1) 
			uncList.append(unc)
	for i in range( len (yList)):
		plt.plot( xList[i], yList[i], color = colorList[i], label = titList[i], linestyle='',marker='.', markersize = 10, mec='black' )
		plt.errorbar(xList[i], yList[i], yerr=uncList[i], color=colorList[i], linestyle='', capsize=2)
	
		ax = plt.gca()
		ax.set_ylim( [0, .8] )

	z = np.linspace( .3, 1., 500 )
	plt.plot( z, ff(z), color = 'black', linestyle = '--')
	plt.xlabel(r'$z$')
	plt.ylabel(r'$r$')
	plt.legend()
	plt.savefig('{0}_{1}.pdf'.format(outFileName, i), bbox_inches='tight')
	

def makeWeights( nXbBins, nQ2x, nQ2y,  pathTofile, fileBase , wType, corrType, bin_num):
	colorList = ['red', 'blue', 'magenta', 'green', 'gold', 'cyan', 'black', 'blueviolet','darkorange', 'brown']

	fig,axs = plt.subplots( nQ2x, nQ2y,figsize=(18, 10))
	plt.subplots_adjust( wspace=.1, hspace=.1 )
	i = 0
	yMax =0
	p_bin = [1.25, 2.00, 2.50, 3.5, 5.00]

	for xPlot in range( nQ2x ):
		for yPlot in range( nQ2y ):
			i = i + 1
			
			xList = []
			yList = []	
			uncList = []
	
			for nXb in range(nXbBins):
				with open( 'csvFiles/corrections/{0}/{1}_q2_{2}_xB_{3}.csv'.format(pathTofile, fileBase, i, nXb + 1,'r')) as csvfile: 
					plots = csv.reader(csvfile, delimiter = '\t') 
					x1 = []
					y1 = []
					unc = []

					for row in plots: 
		
						x1.append(float(row[0])) 
						y1.append(float(row[1]))
						unc.append(float(row[2]))
					
					xList.append(x1)
					yList.append(y1) 
					uncList.append(unc)

			#for yDat in yList:
				#if math.isfinite(max(yDat)) and max(yDat) > yMax:
					#yMax = max(yDat)


			
			for j in range ( len ( yList ) ):
				axs[xPlot, yPlot].plot( xList[j], yList[j], colorList[j], marker = '.', linestyle='none', label = r'%0.2f $< x_B <$ %0.2f'%(.1+0.05*j, .1 + 0.05*(j+1)), ms=15, mec='black' )
				axs[xPlot, yPlot].errorbar(xList[j], yList[j], yerr=uncList[j], color = colorList[j], linestyle = '',capsize = 2, lw = 1, capthick = 1)

			textHeight = 0.4
			if( ( wType == 'w+' or wType == 'w-' ) and corrType == 'acc'):
				textHeight = 5 
			axs[xPlot, yPlot].text(.75, textHeight, r'%.1f $< Q^2 <$ %.1f'%(2 + .5*(i-1), 2+.5*(i)), fontsize=12)
			
			if corrType == 'kaon':
				axs[xPlot, yPlot].text(.75, textHeight - .1, r'%.2f $< p_{\pi} <$ %.2f'%( p_bin[bin_num], p_bin[bin_num+1]), fontsize=12)
				

	folder = 'correction_ratios'
	if corrType == 'acc':
		if wType == 'w+/w-':
			yMax = 1.5
		else:
			yMax = 12. #8
			folder = 'acceptance_corrections'
	elif corrType == 'bin_migrations':
		if wType == 'w+/w-':
			yMax = 1.5
		else:
			yMax = 2.5
			folder = 'bin_migrations'
	else:
		folder = 'kaon_corrections'
		if wType == 'w+/w-':
			yMax = 1.25
		else:
			yMax = 1.05
			folder = 'kaon_corrections'
		

	for ax in axs.flat:
		ax.set_xlabel( getTitle('Z'), fontsize=16 )
		ax.set_ylabel( getTitle(wType), fontsize=16)
		ax.label_outer()
	
		ax.set_ylim( [0, yMax] )
		ax.set_xlim( [0.3, 1] )
	
	for xPlot in range( nQ2x ):
		for yPlot in range( nQ2y ):
		
			axs[xPlot, yPlot].axhline( y = 1, color = 'black', linestyle = '--')
	axs[0,1].legend(loc='upper center', bbox_to_anchor=(0.5, 1.5), ncol=5, fancybox=True, shadow=True)	
			
	
	plt.savefig('PDFs/{4}/{0}_{1}_q2_{2}_xB_{3}.pdf'.format(pathTofile, fileBase, i, nXb + 1, folder, 'r'), bbox_inches='tight')


def plotWeightUncertainties( nXbBins, nQ2x, nQ2y,  pathTofile, fileBase , wType, corrType):
	colorList = ['red', 'blue', 'magenta', 'green', 'gold', 'cyan', 'black', 'blueviolet','darkorange', 'brown']

	fig,axs = plt.subplots( nQ2x, nQ2y,figsize=(18, 10))
	plt.subplots_adjust( wspace=.1, hspace=.1 )
	i = 0
	yMax =0

	for xPlot in range( nQ2x ):
		for yPlot in range( nQ2y ):
			i = i + 1
			
			xList = []
			yList = []	
			uncList = []
	
			for nXb in range(nXbBins):
				with open( 'csvFiles/corrections/{0}/{1}_q2_{2}_xB_{3}.csv'.format(pathTofile, fileBase, i, nXb + 1,'r')) as csvfile: 
					plots = csv.reader(csvfile, delimiter = '\t') 
					x1 = []
					y1 = []
					unc = []

					for row in plots: 
		
						x1.append(float(row[0])) 
						y1.append(float(row[1]))
						unc.append(float(row[2]))
					
					xList.append(x1)
					yList.append(y1) 
					uncList.append(unc)

			#for yDat in yList:
			plt.text(.725, .5, r'%.2f $< x_B <$ %.2f'%( .1 + .05*xb, .1 + .05*(xb+1) ), fontsize=12)
				#if math.isfinite(max(yDat)) and max(yDat) > yMax:
					#yMax = max(yDat)

			plt.text(.725, .5, r'%.2f $< x_B <$ %.2f'%( .1 + .05*xb, .1 + .05*(xb+1) ), fontsize=12)

			
			for j in range ( len ( yList ) ):
				errRatio = []
				for entry in range( len (yList[j]) ):
					if yList[j][entry] == 0:
						errRatio.append(0)
					else:
						errRatio.append(uncList[j][entry]) #/ yList[j][entry])

				axs[xPlot, yPlot].plot( xList[j], errRatio, colorList[j], marker = '.', markersize = 10, linestyle='none', label = r'%0.2f $< x_B <$ %0.2f'%(.1+0.05*j, .1 + 0.05*(j+1)), mec='black' )
			textHeight = .4	

			if wType == 'w+/w-':
				textHeight = .8
			
			axs[xPlot, yPlot].text(.575,textHeight, r'%.1f $< Q^2 <$ %.1f [GeV$^2$]'%(2 + .5*(i-1), 2+.5*(i)), fontsize=12)
			
			if wType == 'w+' or wType == 'w-':
				axs[xPlot, yPlot].axhline( y = .2, color = 'black', linestyle = '--')


	if corrType == 'acc':
		if wType == 'w+/w-':
			yMax = 1
		else:
			yMax = .5
	else:
		if wType == 'w+/w-':
			yMax = 1.
		else:
			yMax = .5
		

	for ax in axs.flat:
		ax.set_xlabel( getTitle('Z'), fontsize=15 )
		ax.set_ylabel(r'$\Delta$('+ getTitle(wType) + ')/(' + getTitle(wType) + ')' , fontsize=15)
		ax.label_outer()
	
		ax.set_ylim( [0., yMax] )
		ax.set_xlim( [0.3, 1] )
	
	
	axs[0,1].legend(loc='upper center', bbox_to_anchor=(0.5, 1.5), ncol=5)#, fancybox=True, shadow=True)	
			
	plt.savefig('PDFs/corrections/{0}/uncertainty_{1}_q2_{2}_xB_{3}.pdf'.format(pathTofile, fileBase, i, nXb + 1,'r'), bbox_inches='tight')

def makeAllWeights(inFileName):
	makeWeights( 10, 4, 3,  '{0}'.format(inFileName), 'acceptance_corrections' , 'w+/w-', 'acc')
	makeWeights( 10, 4, 3,  '{0}'.format(inFileName), 'acceptance_corrections_pip' , 'w+', 'acc')
	makeWeights( 10, 4, 3,  '{0}'.format(inFileName), 'acceptance_corrections_pim' , 'w-', 'acc')
	
	makeWeights( 10, 4, 3,  '{0}'.format(inFileName), 'bin_migration' , 'w+/w-', 'bin')
	makeWeights( 10, 4, 3,  '{0}'.format(inFileName), 'bin_migration_pip' , 'w+', 'bin')
	makeWeights( 10, 4, 3,  '{0}'.format(inFileName), 'bin_migration_pim' , 'w-', 'bin')
	
def makeKaonWeights(inFileName):
	
	for i in range(4):
		makeWeights( 10, 4, 3,  '{0}'.format(inFileName), 'kaon_correction_{0}'.format(i) , 'w+/w-', 'kaon', i)
		makeWeights( 10, 4, 3,  '{0}'.format(inFileName), 'kaon_correction_pip_{0}'.format(i) , 'w+', 'kaon', i)
		makeWeights( 10, 4, 3,  '{0}'.format(inFileName), 'kaon_correction_pim_{0}'.format(i) , 'w-', 'kaon', i)

def makeAllUncertainties(inFileName):
	plotWeightUncertainties( 10, 4, 3,  'csvFiles/corrections/{0}'.format(inFileName), 'acceptance_corrections' , 'w+/w-', 'acc')
	plotWeightUncertainties( 10, 4, 3,  'csvFiles/corrections/{0}'.format(inFileName), 'acceptance_corrections_pip' , 'w+', 'acc')
	plotWeightUncertainties( 10, 4, 3,  'csvFiles/corrections/{0}'.format(inFileName), 'acceptance_corrections_pim' , 'w-', 'acc')
	
	plotWeightUncertainties( 10, 4, 3,  'csvFiles/corrections/{0}'.format(inFileName), 'bin_migration' , 'w+/w-', 'bin')
	plotWeightUncertainties( 10, 4, 3,  'csvFiles/corrections/{0}'.format(inFileName), 'bin_migration_pip' , 'w+', 'bin')
	plotWeightUncertainties( 10, 4, 3,  'csvFiles/corrections/{0}'.format(inFileName), 'bin_migration_pim' , 'w-', 'bin')


def makeAllRatioBinned( fileList , titList, outFileName):
	colorList = ['red', 'blue', 'green', 'darkorange', 'cyan', 'black', 'blueviolet','darkorange', 'brown']

	for q2 in range(12):
		for xb in range(10):


			xList = []
			yList = []	
			uncList = []

			i = 0
			for file in fileList:
				with open( 'csvFiles/ratios/{0}/ratio_{1}_{2}.csv'.format(file, q2+1, xb+1) ,'r') as csvfile: 
					plots = csv.reader(csvfile, delimiter = '\t') 
					x1 = []
					y1 = []
					unc = []

					for row in plots: 
			
						x1.append(float(row[0]) + 0.005*i ) 
						y1.append(float(row[1]))
						unc.append(float(row[2]))
					
					i = i+1
					xList.append(x1)
					yList.append(y1) 
					uncList.append(unc)
			isPlot = False

			for i in range( len (yList)):
				if sum( yList[i] ) > -56.0:
					isPlot = True
					plt.plot( xList[i], yList[i], color = colorList[i], label = titList[i], linestyle='',marker='.', markersize = 10, mec='black' )
					plt.errorbar(xList[i], yList[i], yerr=uncList[i], color=colorList[i], linestyle='', capsize=2)
			
					ax = plt.gca()
					ax.set_ylim( [0, .8] )

			if isPlot == True:
				z = np.linspace( .3, 1., 500 )
				plt.plot( z, ff(z), color = 'black', linestyle = '--')
				plt.xlabel(r'$z$')
				plt.ylabel(r'$r$')
				plt.text(.725, .55, r'%.1f $< Q^2 <$ %.1f [GeV$^2$]'%(2 + .5*(q2), 2+.5*(q2+1) ), fontsize=12)
				plt.text(.725, .5, r'%.2f $< x_B <$ %.2f'%( .1 + .05*xb, .1 + .05*(xb+1) ), fontsize=12)
				plt.legend()
				#plt.show()
				plt.savefig('PDFs/ratios/{0}/ratio_{2}_{1}.pdf'.format(outFileName, q2+1, xb+1), bbox_inches='tight')
			
			plt.clf()

def makeRatioRatioBinned( fileList , titList, outFileName):
	colorList = ['blue', 'blue', 'green', 'cyan', 'black', 'blueviolet','darkorange', 'brown']

	for q2 in range(12):
		for xb in range(10):


			xList = []
			yList = []	
			uncList = []
	
			i = 0

			for file in fileList:
				with open( 'csvFiles/ratios/{0}/ratio_{1}_{2}.csv'.format(file, q2+1, xb+1) ,'r') as csvfile: 
					plots = csv.reader(csvfile, delimiter = '\t') 
					x1 = []
					y1 = []
					unc = []

					for row in plots: 
			
						x1.append(float(row[0])+ .005*i) 
						y1.append(float(row[1]))
						unc.append(float(row[2]))

					i = i + 1
					xList.append(x1)
					yList.append(y1) 
					uncList.append(unc)
			isPlot = False

			for i in range( len (yList) - 1 ):
				if sum( yList[i+1] ) > -56.0 and sum( yList[0] ) > -56.0:
					isPlot = True
					plt.plot( xList[i+1], divide_lists( yList[i+1], yList[0] ), color = colorList[i+1], label = titList[i+1], linestyle='',marker='.', markersize = 10, mec='black' )
					plt.errorbar(xList[i+1],divide_lists( yList[i+1], yList[0] ), yerr=prop_err( yList[i+1], yList[0], uncList[i+1], uncList[0] ), color=colorList[i+1], linestyle='', capsize=2)
			
				

					ax = plt.gca()
					ax.set_ylim( [0.75, 1.25] )
					ax.set_xlim( [.3, .7] )

			if isPlot == True:
				plt.axhline( y = 1., color = 'black', linestyle = '--')
				plt.xlabel(r'$z$')
				plt.ylabel('Ratio')
				plt.text(.525, 1.15, r'%.1f $< Q^2 <$ %.1f [GeV$^2$]'%(2 + .5*(q2), 2+.5*(q2+1) ), fontsize=12)
				plt.text(.525, 1.125, r'%.2f $< x_B <$ %.2f'%( .1 + .05*xb, .1 + .05*(xb+1) ), fontsize=12)
				plt.legend()
				#plt.show()
				plt.savefig('PDFs/ratios/{0}/double_ratio_{1}_{2}.pdf'.format(outFileName, q2+1, xb+1), bbox_inches='tight')
			
			plt.clf()


def makeAllRatioBinnedXb( file , outFileName):
	colorList = ['red', 'blue', 'green', 'darkorange', 'cyan', 'blueviolet', 'magenta','darkorange', 'brown', 'black']

	for q2 in range(12):
		titList = []
		xList = []
		yList = []	
		uncList = []
		for xb in range(10):


			i = 0
			with open( 'csvFiles/ratios/{0}/ratio_{1}_{2}.csv'.format(file, q2+1, xb+1) ,'r') as csvfile: 
				plots = csv.reader(csvfile, delimiter = '\t') 
				x1 = []
				y1 = []
				unc = []

				for row in plots: 
			
					x1.append(float(row[0]) + 0.005*i ) 
					y1.append(float(row[1]))
					unc.append(float(row[2]))
				
				i = i+1
				xList.append(x1)
				yList.append(y1) 
				uncList.append(unc)
				titList.append(r'%.2f $< x_B <$ %.2f'%( .1 + .05*xb, .1 + .05*(xb+1)) )  

		for i in range( len (yList)):
			if sum( yList[i] ) > -56.0:
				plt.plot( xList[i], yList[i], color = colorList[i], label = titList[i], linestyle='',marker='.', markersize = 10, mec='black' )
				plt.errorbar(xList[i], yList[i], yerr=uncList[i], color=colorList[i], linestyle='', capsize=2)
		
				ax = plt.gca()
				ax.set_ylim( [0, .8] )

		z = np.linspace( .3, 1., 500 )
		plt.plot( z, ff(z), color = 'black', linestyle = '--')
		plt.xlabel(r'$z$')
		plt.ylabel(r'$r$')
		plt.text(.725, .55, r'%.1f $< Q^2 <$ %.1f [GeV$^2$]'%(2 + .5*(q2), 2+.5*(q2+1) ), fontsize=12)
		plt.legend()
				#plt.show()
		plt.savefig('PDFs/ratios/{0}/ratio_{1}_{2}.pdf'.format(outFileName, q2+1, xb+1), bbox_inches='tight')
			
		plt.clf()

def makeAllRatioBinnedQ2( file , outFileName):
	colorList = ['red', 'blue', 'green', 'darkorange', 'cyan', 'blueviolet', 'magenta','darkorange', 'brown', 'black', 'yellow', 'gray']

	for xb in range(10):
		titList = []
		xList = []
		yList = []	
		uncList = []
		for q2 in range(12):


			i = 0
			with open( 'csvFiles/ratios/{0}/ratio_{1}_{2}.csv'.format(file, q2+1, xb+1) ,'r') as csvfile: 
				plots = csv.reader(csvfile, delimiter = '\t') 
				x1 = []
				y1 = []
				unc = []

				for row in plots: 
			
					x1.append(float(row[0]) + 0.005*i ) 
					y1.append(float(row[1]))
					unc.append(float(row[2]))
				
				i = i+1
				xList.append(x1)
				yList.append(y1) 
				uncList.append(unc)
				titList.append(r'%.1f $< Q^2 <$ %.1f [GeV$^2$]'%( 2 + .5*q2, 2 + .5*(q2+1)) )  

		for i in range( len (yList)):
			if sum( yList[i] ) > -56.0:
				plt.plot( xList[i], yList[i], color = colorList[i], label = titList[i], linestyle='',marker='.', markersize = 10, mec='black' )
				plt.errorbar(xList[i], yList[i], yerr=uncList[i], color=colorList[i], linestyle='', capsize=2)
		
				ax = plt.gca()
				ax.set_ylim( [0, .8] )

		z = np.linspace( .3, 1., 500 )
		plt.plot( z, ff(z), color = 'black', linestyle = '--')
		plt.xlabel(r'$z$')
		plt.ylabel(r'$r$')
		plt.text(.775, .40, r'%.2f $< x_B <$ %.2f'%(.1 + .05*(xb), .1+.05*(xb+1) ), fontsize=12)
		plt.legend()
				#plt.show()
		plt.savefig('PDFs/ratios/{0}/ratio_{1}_{2}.pdf'.format(outFileName, q2+1, xb+1), bbox_inches='tight')
			
		plt.clf()

def makeAllRatioBinned3D( file , outFileName, nBins):
	colorList = ['red', 'blue', 'green', 'darkorange', 'cyan', 'blueviolet', 'magenta','darkorange', 'brown', 'black', 'yellow', 'gray']

	for xb in range(5):
		titList = []
		xList = []
		yList = []	
		uncList = []
		for q2 in range(4):

			for bin3 in range( nBins ):
				i = 0
				with open( 'csvFiles/ratios/{0}/ratio_{1}_{2}_{3}.csv'.format(file, q2+1, xb+1, bin3+1) ,'r') as csvfile: 
					plots = csv.reader(csvfile, delimiter = '\t') 
					x1 = []
					y1 = []
					unc = []

					for row in plots: 
				
						x1.append(float(row[0]) + 0.005*i ) 
						y1.append(float(row[1]))
						unc.append(float(row[2]))
					
					i = i+1
					xList.append(x1)
					yList.append(y1) 
					uncList.append(unc)
					titList.append(r'%.1f $< Q^2 <$ %.1f [GeV$^2$]'%( 2 + .5*q2, 2 + .5*(q2+1)) )  

			for i in range( len (yList)):
				if sum( yList[i] ) > -56.0:
					plt.plot( xList[i], yList[i], color = colorList[i], label = titList[i], linestyle='',marker='.', markersize = 10, mec='black' )
					plt.errorbar(xList[i], yList[i], yerr=uncList[i], color=colorList[i], linestyle='', capsize=2)
			
					ax = plt.gca()
					ax.set_ylim( [0, .8] )

			z = np.linspace( .3, 1., 500 )
			plt.plot( z, ff(z), color = 'black', linestyle = '--')
			plt.xlabel(r'$z$')
			plt.ylabel(r'$r$')
			plt.text(.775, .40, r'%.2f $< x_B <$ %.2f'%(.1 + .05*(xb), .1+.05*(xb+1) ), fontsize=12)
			plt.text(.775, .45, r'%.2f $< Q^2 <$ %.2f'%(2 + .5*(q2), 2+.5*(q2+1) ), fontsize=12)
			plt.legend()
					#plt.show()
			plt.savefig('PDFs/ratios/{0}/ratio_{1}_{2}_{3}.pdf'.format(outFileName, q2+1, xb+1, nBins+1), bbox_inches='tight')
				
			plt.clf()
