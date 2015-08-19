# -*- coding: utf-8 -*-
"""
/***************************************************************************
 satsviz
                                 A QGIS plugin
 SaTSViz aims to provide QGIS an additional feature of analysis by utilising SaTScan. All input files needed for SaTScan are created by the plugin and the output files from it are read by the plugin and fed in to QGIS to visualise the analysis results. The plugin provides benefit to both the software's
                              -------------------
        begin                : 2015-06-24
        git sha              : $Format:%H$
        copyright            : (C) 2015 by by Vasuda Trehan under guidance of Shiva Reddy Koti
        email                : vasudatrehan@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from detect_satsviz_dialog import satsvizDialog
import os.path
from qgis.core import *
from qgis.gui import *
import qgis.utils
import os
import subprocess
import tempfile


tempd = os.path.expanduser("~")
temp= os.path.join(tempd,"temp23.prm")


#temp= tempfile.NamedTemporaryFile(suffix='.prm').name
#temp= "C://Users//sony//temp.prm"
class satsviz:
    
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface        
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'satsviz_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = satsvizDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&SaTSViz')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'satsviz')
        self.toolbar.setObjectName(u'satsviz')

    # noinspection PyMethodMayBeStatic
    
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('satsviz', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/satsviz/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'satsviz'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&SaTSViz'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
        
    def call(self,sat_path): #Batch File
        tempcall= os.path.expanduser("~")
        tempcfile= os.path.join(tempcall,'temp23.prm')
     #Call SaTScan for analysis	
        subprocess.call([sat_path,tempcfile])
     #this program contains code to create parameter file for input of shape file in satscan    
        
    def write_session(self,file_path,cas_attr_col_num,ctl_attr_col_num,s_date,e_date,pop_col_num,coord_col_num,output_path):
        path=file_path
        cascolnum=cas_attr_col_num
        ctlcolnum=ctl_attr_col_num
        popcolnum=pop_col_num
        geoattrnum=coord_col_num
        fo=open(temp,"w+")
        fo.write("""[Input]
        
;case data filename
CaseFile="""+path+"""
;source type (CSV=0, DBASE=1, SHAPE=2)
CaseFile-SourceType=2
;source field map (comma separated list of integers, oneCount, generatedId, shapeX, shapeY)
CaseFile-SourceFieldMap="""+str(geoattrnum)+""","""+str(cascolnum)+"""
;control data filename
ControlFile=ControlFile="""+path+"""
;source type (CSV=0, DBASE=1, SHAPE=2)
ControlFile-SourceType=2
;source field map (comma separated list of integers, oneCount, generatedId, shapeX, shapeY)
ControlFile-SourceFieldMap="""+str(geoattrnum)+""","""+str(ctlcolnum)+"""
;time precision (0=None, 1=Year, 2=Month, 3=Day, 4=Generic)
PrecisionCaseTimes=0
;study period start date (YYYY/MM/DD)
StartDate="""+s_date.toString("yyyy/MM/dd")+"""
;study period end date (YYYY/MM/DD)
EndDate="""+e_date.toString("yyyy/MM/dd")+"""
;population data filename
PopulationFile="""+path+"""
;source type (CSV=0, DBASE=1, SHAPE=2)
PopulationFile-SourceType=2
;source field map (comma separated list of integers, oneCount, generatedId, shapeX, shapeY)
PopulationFile-SourceFieldMap="""+str(geoattrnum)+""",unspecifiedPopDate,"""+str(popcolnum)+"""
;coordinate data filename
CoordinatesFile="""+path+"""
;source type (CSV=0, DBASE=1, SHAPE=2)
CoordinatesFile-SourceType=2
;source field map (comma separated list of integers, oneCount, generatedId, shapeX, shapeY)
CoordinatesFile-SourceFieldMap="""+str(geoattrnum)+""",shapeX,shapeY
;use grid file? (y/n)
UseGridFile=n
;grid data filename
GridFile=
;coordinate type (0=Cartesian, 1=latitude/longitude)
CoordinatesType=1

[Analysis]
;analysis type (1=Purely Spatial, 2=Purely Temporal, 3=Retrospective Space-Time, 4=Prospective Space-Time, 5=Spatial Variation in Temporal Trends, 6=Prospective Purely Temporal)
AnalysisType=1
;model type (0=Discrete Poisson, 1=Bernoulli, 2=Space-Time Permutation, 3=Ordinal, 4=Exponential, 5=Normal, 6=Continuous Poisson, 7=Multinomial)
ModelType=0
;scan areas (1=High Rates(Poison,Bernoulli,STP); High Values(Ordinal,Normal); Short Survival(Exponential), 2=Low Rates(Poison,Bernoulli,STP); Low Values(Ordinal,Normal); Long Survival(Exponential), 3=Both Areas)
ScanAreas=1
;time aggregation units (0=None, 1=Year, 2=Month, 3=Day, 4=Generic)
TimeAggregationUnits=1
;time aggregation length (Positive Integer)
TimeAggregationLength=1

[Output]
;analysis main results output filename
ResultsFile="""+output_path+"""
;output Google Earth KML file (y/n)
OutputGoogleEarthKML=n
;output shapefiles (y/n)
OutputShapefiles=y
;output cluster information in ASCII format? (y/n)
MostLikelyClusterEachCentroidASCII=n
;output cluster information in dBase format? (y/n)
MostLikelyClusterEachCentroidDBase=y
;output cluster case information in ASCII format? (y/n)
MostLikelyClusterCaseInfoEachCentroidASCII=n
;output cluster case information in dBase format? (y/n)
MostLikelyClusterCaseInfoEachCentroidDBase=y
;output location information in ASCII format? (y/n)
CensusAreasReportedClustersASCII=n
;output location information in dBase format? (y/n)
CensusAreasReportedClustersDBase=y
;output risk estimates in ASCII format? (y/n)
IncludeRelativeRisksCensusAreasASCII=n
;output risk estimates in dBase format? (y/n)
IncludeRelativeRisksCensusAreasDBase=y
;output simulated log likelihoods ratios in ASCII format? (y/n)
SaveSimLLRsASCII=n
;output simulated log likelihoods ratios in dBase format? (y/n)
SaveSimLLRsDBase=y

[Multiple Data Sets]
; multiple data sets purpose type (0=Multivariate, 1=Adjustment)
MultipleDataSetsPurposeType=0

[Data Checking]
;study period data check (0=Strict Bounds, 1=Relaxed Bounds)
StudyPeriodCheckType=0
;geographical coordinates data check (0=Strict Coordinates, 1=Relaxed Coordinates)
GeographicalCoordinatesCheckType=0

[Spatial Neighbors]
;use neighbors file (y/n)
UseNeighborsFile=n
;neighbors file
NeighborsFilename=
;use meta locations file (y/n)
UseMetaLocationsFile=n
;meta locations file
MetaLocationsFilename=
;multiple coordinates type (0=OnePerLocation, 1=AtLeastOneLocation, 2=AllLocations)
MultipleCoordinatesType=0

[Spatial Window]
;maximum spatial size in population at risk (<=50%)
MaxSpatialSizeInPopulationAtRisk=50
;restrict maximum spatial size - max circle file? (y/n)
UseMaxCirclePopulationFileOption=n
;maximum spatial size in max circle population file (<=50%)
MaxSpatialSizeInMaxCirclePopulationFile=50
;maximum circle size filename
MaxCirclePopulationFile=
;restrict maximum spatial size - distance? (y/n)
UseDistanceFromCenterOption=n
;maximum spatial size in distance from center (positive integer)
MaxSpatialSizeInDistanceFromCenter=1
;include purely temporal clusters? (y/n)
IncludePurelyTemporal=n
;window shape (0=Circular, 1=Elliptic)
SpatialWindowShapeType=0
;elliptic non-compactness penalty (0=NoPenalty, 1=MediumPenalty, 2=StrongPenalty)
NonCompactnessPenalty=1
;isotonic scan (0=Standard, 1=Monotone)
IsotonicScan=0

[Temporal Window]
;minimum temporal cluster size (in time aggregation units)
MinimumTemporalClusterSize=1
;how max temporal size should be interpretted (0=Percentage, 1=Time)
MaxTemporalSizeInterpretation=0
;maximum temporal cluster size (<=90%)
MaxTemporalSize=50
;include purely spatial clusters? (y/n)
IncludePurelySpatial=n
;temporal clusters evaluated (0=All, 1=Alive, 2=Flexible Window)
IncludeClusters=0
;flexible temporal window start range (YYYY/MM/DD,YYYY/MM/DD)
IntervalStartRange=2000/1/1,2000/12/31
;flexible temporal window end range (YYYY/MM/DD,YYYY/MM/DD)
IntervalEndRange=2000/1/1,2000/12/31

[Space and Time Adjustments]
;time trend adjustment type (0=None, 1=Nonparametric, 2=LogLinearPercentage, 3=CalculatedLogLinearPercentage, 4=TimeStratifiedRandomization, 5=CalculatedQuadraticPercentage)
TimeTrendAdjustmentType=0
;time trend adjustment percentage (>-100)
TimeTrendPercentage=0
;time trend type - SVTT only (Linear=0, Quadratic=1)
TimeTrendType=0
;adjust for weekly trends, nonparametric
AdjustForWeeklyTrends=n
;spatial adjustments type (0=No Spatial Adjustment, 1=Spatially Stratified Randomization)
SpatialAdjustmentType=0
;use adjustments by known relative risks file? (y/n)
UseAdjustmentsByRRFile=n
;adjustments by known relative risks file name (with HA Randomization=1)
AdjustmentsByKnownRelativeRisksFilename=

[Inference]
;p-value reporting type (Default p-value=0, Standard Monte Carlo=1, Early Termination=2, Gumbel p-value=3) 
PValueReportType=0
;early termination threshold
EarlyTerminationThreshold=50
;report Gumbel p-values (y/n)
ReportGumbel=n
;Monte Carlo replications (0, 9, 999, n999)
MonteCarloReps=999
;adjust for earlier analyses(prospective analyses only)? (y/n)
AdjustForEarlierAnalyses=n
;prospective surveillance start date (YYYY/MM/DD)
ProspectiveStartDate=2000/12/31
;perform iterative scans? (y/n)
IterativeScan=n
;maximum iterations for iterative scan (0-32000)
IterativeScanMaxIterations=10
;max p-value for iterative scan before cutoff (0.000-1.000)
IterativeScanMaxPValue=0.05

[Border Analysis]
;calculate Oliveira's F
CalculateOliveira=n
;number of bootstrap replications for Oliveira calculation (minimum=100, multiple of 100)
NumBootstrapReplications=1000
;p-value cutoff for cluster's in Oliveira calculation (0.000-1.000)
OliveiraPvalueCutoff=0.05

[Power Evaluation]
;perform power evaluation - Poisson only (y/n)
PerformPowerEvaluation=n
;power evaluation method (0=Analysis And Power Evaluation Together, 1=Only Power Evaluation With Case File, 2=Only Power Evaluation With Defined Total Cases)
PowerEvaluationsMethod=0
;total cases in power evaluation
PowerEvaluationTotalCases=600
;critical value type (0=Monte Carlo, 1=Gumbel, 2=User Specified Values)
CriticalValueType=0
;power evaluation critical value .05 (> 0)
CriticalValue05=0
;power evaluation critical value .001 (> 0)
CriticalValue01=0
;power evaluation critical value .001 (> 0)
CriticalValue001=0
;power estimation type (0=Monte Carlo, 1=Gumbel)
PowerEstimationType=0
;number of replications in power step
NumberPowerReplications=1000
;power evaluation alternative hypothesis filename
AlternativeHypothesisFilename=
;power evaluation simulation method for power step (0=Null Randomization, 1=N/A, 2=File Import)
PowerEvaluationsSimulationMethod=0
;power evaluation simulation data source filename
PowerEvaluationsSimulationSourceFilename=
;report power evaluation randomization data from power step (y/n)
ReportPowerEvaluationSimulationData=n
;power evaluation simulation data output filename
PowerEvaluationsSimulationOutputFilename=

[Spatial Output]
;automatically launch Google Earth - gui only (y/n)
LaunchKMLViewer=y
;create compressed KMZ file instead of KML file (y/n)
CompressKMLtoKMZ=n
;whether to include cluster locations kml output (y/n)
IncludeClusterLocationsKML=y
;threshold for generating separate kml files for cluster locations (positive integer)
ThresholdLocationsSeparateKML=1000
;report hierarchical clusters (y/n)
ReportHierarchicalClusters=y
;criteria for reporting secondary clusters(0=NoGeoOverlap, 1=NoCentersInOther, 2=NoCentersInMostLikely,  3=NoCentersInLessLikely, 4=NoPairsCentersEachOther, 5=NoRestrictions)
CriteriaForReportingSecondaryClusters=0
;report gini clusters (y/n)
ReportGiniClusters=y
;gini index cluster reporting type (0=optimal index only, 1=all values)
GiniIndexClusterReportingType=0
;spatial window maxima stops (comma separated decimal values[<=50%] )
SpatialMaxima=1,2,3,4,5,6,8,10,12,15,20,25,30,40,50
;max p-value for clusters used in calculation of index based coefficients (0.000-1.000)
GiniIndexClustersPValueCutOff=0.05
;report gini index coefficents to results file (y/n)
ReportGiniIndexCoefficents=n
;restrict reported clusters to maximum geographical cluster size? (y/n)
UseReportOnlySmallerClusters=n
;maximum reported spatial size in population at risk (<=50%)
MaxSpatialSizeInPopulationAtRisk_Reported=50
;restrict maximum reported spatial size - max circle file? (y/n)
UseMaxCirclePopulationFileOption_Reported=n
;maximum reported spatial size in max circle population file (<=50%)
MaxSizeInMaxCirclePopulationFile_Reported=50
;restrict maximum reported spatial size - distance? (y/n)
UseDistanceFromCenterOption_Reported=n
;maximum reported spatial size in distance from center (positive integer)
MaxSpatialSizeInDistanceFromCenter_Reported=1

[Temporal Output]
;output temporal graph HTML file (y/n)
OutputTemporalGraphHTML=n
;temporal graph cluster reporting type (0=Only most likely cluster, 1=X most likely clusters, 2=Only significant clusters)
TemporalGraphReportType=0
;number of most likely clusters to report in temporal graph (positive integer)
TemporalGraphMostMLC=1
;significant clusters p-value cutoff to report in temporal graph (0.000-1.000)
TemporalGraphSignificanceCutoff=0.05

[Other Output]
;report critical values for .01 and .05? (y/n)
CriticalValue=n
;report cluster rank (y/n)
ReportClusterRank=n
;print ascii headers in output files (y/n)
PrintAsciiColumnHeaders=n
;user-defined title for results file
ResultsTitle=

[Elliptic Scan]
;elliptic shapes - one value for each ellipse (comma separated decimal values)
EllipseShapes=1.5,2,3,4,5
;elliptic angles - one value for each ellipse (comma separated integer values)
EllipseAngles=4,6,9,12,15

[Power Simulations]
;simulation methods (0=Null Randomization, 1=N/A, 2=File Import)
SimulatedDataMethodType=0
;simulation data input file name (with File Import=2)
SimulatedDataInputFilename=
;print simulation data to file? (y/n)
PrintSimulatedDataToFile=n
;simulation data output filename
SimulatedDataOutputFilename=

[Run Options]
;number of parallel processes to execute (0=All Processors, x=At Most X Processors)
NumberParallelProcesses=0
;suppressing warnings? (y/n)
SuppressWarnings=n
;log analysis run to history file? (y/n)
LogRunToHistoryFile=y
;analysis execution method  (0=Automatic, 1=Successively, 2=Centrically)
ExecutionType=0

[System]
;system setting - do not modify

        Version=9.4.1""");
        fo.close()
        
    

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show() 
        self.dlg.comboBox_5.clear()   #if we were not having clear command then it will come again and again teh same file
        layers=qgis.utils.iface.legendInterface().layers()
        for layer in layers:          # iterating the no of layers
           self.dlg.comboBox_5.addItem(layer.name())  # adding different layers in the combo box

           
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:            
            i=self.dlg.comboBox_5.currentIndex()
            path=layers[i].source()

            cascolnum=self.dlg.comboBox.currentIndex()     #case
            
            ctlcolnum=self.dlg.comboBox_2.currentIndex()   #control

            s_date=self.dlg.dateEdit.date()   # start date

            e_date=self.dlg.dateEdit_2.date()   #end date

            popcolnum=self.dlg.comboBox_3.currentIndex()#population

            geoattrnum=self.dlg.comboBox_4.currentIndex()    #coordinate
            
            output_path=self.dlg.lineEdit.text()#output\
            output_path=output_path.replace('/',r'\\')
    
            self.write_session(path,cascolnum,ctlcolnum,s_date,e_date,popcolnum,geoattrnum,output_path)
            self.call("C:\\Program Files\\SaTScan\\SatScanBatch64.exe")            
            n=output_path[:-4]+".col.shp"          

            qgis.utils.iface.addVectorLayer(n,"output",'ogr')

            
            
  
