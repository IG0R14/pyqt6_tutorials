import sys
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class Title(QLabel):
    
    def __init__(self, title):
        super().__init__()
        
        self.setText(title)
        self.setFont(QFont("Courier New", 11))
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setObjectName('title')
        self.setStyleSheet('''
                            #title {
                                color: #004d00;
                                font-weight: bold;
                            }
                            ''')

class Label(QLabel):
    
    def __init__(self, text):
        super().__init__()
        
        self.setText(text)
        self.setFont(QFont("Arial", 10))
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.setObjectName('label')
        self.setStyleSheet('''
                            #label {
                                padding-top: 5px;
                                padding-bottom: 5px;
                                padding-right: 20px;
                            }
                            ''')
        
class DataLabel(QLabel):
    
    def __init__(self, text="N/A"):
        super().__init__()
        
        self.setText(text)
        self.setFont(QFont("Arial", 10))
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setFixedWidth(120)
        self.setObjectName('data-label')
        self.setStyleSheet('''
                            #data-label {
                                background-color: white; 
                                border-radius: 5px; 
                                border-bottom: 1px solid black;  
                                padding: 2px 10px; 
                            }
                            ''')

class Button(QPushButton):
    
    def __init__(self, button_type, name, dimension=[120, 100]):
        super().__init__()
        
        self.button_type = button_type
        self.name = name
        
        self.setText(self.name)
        self.setFont(QFont("Arial", 16))
        self.setFixedWidth(dimension[0])
        self.setFixedHeight(dimension[1])
        self.setObjectName('push-button')
        
        if(self.button_type == 'start'):
            self.setStyleSheet('''
                                #push-button {
                                    border: 1px solid black;
                                    border-radius: 5px;
                                    background-color: #228B22;
                                    margin: 5px;
                                    font-weight: bold;
                                }
                                ''')
        
        if(self.button_type == 'stop'):
            self.setStyleSheet('''
                                border: 1px solid black;
                                border-radius: 5px;
                                background-color: #B22222;
                                margin: 5px;
                                font-weight: bold;
                                ''')
        
        if(self.button_type == 'running'):
            self.setText('running')
            self.setStyleSheet('''
                                border-radius: 5px;
                                background-color: #DAA520;
                                margin: 5px;
                                font-weight: bold;
                                ''')
        

class BidirectionalGridWidget(QFrame):
    
    def __init__(self):
        super().__init__()
        
        self.button1_state = DataLabel('Activated')
        self.button2_state = DataLabel('Deactivated')
        self.cycle_count = DataLabel(str(657))
        self.start_button = Button(button_type='start', name='Start')
        self.stop_button = Button(button_type='stop', name='Stop')
        
        bidirectional_grid = QGridLayout()
        
        bidirectional_grid.addWidget(Label("Button 1 State"), 0, 0)
        bidirectional_grid.addWidget(self.button1_state, 0, 1)
        bidirectional_grid.addWidget(Label("Button 2 State"), 1, 0)
        bidirectional_grid.addWidget(self.button2_state, 1, 1)
        bidirectional_grid.addWidget(Label("Cycle Count"), 2, 0)
        bidirectional_grid.addWidget(self.cycle_count, 2, 1)
        bidirectional_grid.addWidget(self.start_button, 3, 0)
        bidirectional_grid.addWidget(self.stop_button, 3, 1)
        self.setObjectName("bidirectional-grid-widget")
        self.setStyleSheet('''
                            #bidirectional-grid-widget {
                                background-color: #ADFF2F;
                                border: 3px outset grey;
                                border-radius: 5px;
                                margin-right: 10px;
                            } 
                            ''')
        
        self.setLayout(bidirectional_grid)

class BistableGridWidget(QFrame):
    
    def __init__(self):
        super().__init__()
        
        # self.setAutoFillBackground(True)
        
        bistable_grid = QGridLayout()
        
        self.button1_state = DataLabel('Triggered')
        self.button1_voltage = DataLabel(str(24.21) + 'V')
        self.cycle_count = DataLabel(str(4830))
        self.start_button = Button(button_type='start', name='Start')
        self.stop_button = Button(button_type='stop', name='Stop')
        
        bistable_grid.addWidget(Label("Button 1 State"), 0, 0)
        bistable_grid.addWidget(self.button1_state, 0, 1)
        bistable_grid.addWidget(Label("Button 1 voltage"), 1, 0)
        bistable_grid.addWidget(self.button1_voltage, 1, 1)
        bistable_grid.addWidget(Label("Cycle Count"), 2, 0)
        bistable_grid.addWidget(self.cycle_count, 2, 1)
        bistable_grid.addWidget(self.start_button, 3, 0)
        bistable_grid.addWidget(self.stop_button, 3, 1)
        self.setObjectName("bistable-grid-widget")
        
        self.setStyleSheet('''
                            #bistable-grid-widget {
                                background-color: #ADFF2F;
                                border: 3px outset grey;
                                border-radius: 5px;
                            }
                            ''')
        
        self.setLayout(bistable_grid)

############################################################################

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        object data returned containing current state of test

    '''
    # finished = pyqtSignal()
    # error = pyqtSignal(tuple)
    # result = pyqtSignal(object)
    progress = pyqtSignal(object)

class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            # self.signals.result.emit(result)  # Return the result of the processing
            print('results available')
        finally:
            # self.signals.finished.emit()  # Done
            print('finished')

############################################################################

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("Bidirectional and Bistable test rig")
        # self.setFixedSize(QSize(800, 480))
        
        main_layout = QGridLayout()
        
        # Creating instances
        bidirectional_title = Title("Bidirectional Test")
        self.bidirectional_grid_widget = BidirectionalGridWidget()
        bistable_title = Title("Bistable Control Test")
        self.bistable_grid_widget = BistableGridWidget()
        
        # Placing instances into main grid
        main_layout.addWidget(bidirectional_title, 0, 0)
        main_layout.addWidget(self.bidirectional_grid_widget, 1, 0)
        main_layout.addWidget(bistable_title, 0, 1)
        main_layout.addWidget(self.bistable_grid_widget, 1, 1)
        
        # Button functions
        self.bidirectional_grid_widget.start_button.pressed.connect(self.bidirectional_start)
        self.bistable_grid_widget.start_button.pressed.connect(self.bistable_start)
        
        widget = QWidget()
        widget.setLayout(main_layout)
        
        self.setCentralWidget(widget)
        
        # Creating thread pool for managing test threads
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        
        self.setStyleSheet('''
            QMainWindow{
                background-color: #609f60;
            }
            ''')
    
    ######################################### Bidirectional Test
    
    def bidirectional_start(self):
        '''
        Creates an instance, sets up and executes the worker thread for the bidirectional test
        '''
        
        print("bidirectional_start function is called")
        bidirectional_worker = Worker(self.bidirectional_test)
        bidirectional_worker.signals.progress.connect(self.update_bidirectional_progress)
        
        # Execute
        self.threadpool.start(bidirectional_worker)
    
    def bidirectional_test(self, progress_callback):
        '''
        Runs the bidirectional test
        '''
        
        print("bidirectional_test function is called")
        
        current_state ={
            "button1_state": "test",
            "button2_state": "test",
            "cycle_count": "50000"
        }
        
        progress_callback.emit(current_state)
        
        return "Bidirectional test finished. 50,000 cycles completed"
    
    def update_bidirectional_progress(self, current_state):
        '''
        Updates the gui for the bidirectional test rig
        '''
        
        print("update_bidirectional_progress function is called")
        self.bidirectional_grid_widget.button1_state.setText(current_state['button1_state'])
        self.bidirectional_grid_widget.button2_state.setText(current_state['button2_state'])
        self.bidirectional_grid_widget.cycle_count.setText(current_state['cycle_count'])
    
    ######################################### Bistable Test
    
    def bistable_start(self):
        '''
        Creates an instance, sets up and executes the worker thread for the bistable test
        '''
        print("bistable_start function is called")
        bistable_worker = Worker(self.bistable_test)
        bistable_worker.signals.progress.connect(self.bistable_progress_update)
        
        self.threadpool.start(bistable_worker)
    
    def bistable_test(self, progress_callback):
        '''
        Runs the bistable test
        '''
        print("bistable_test function is called")
        current_state ={
            "button1_state": "test",
            "button1_voltage": "24.05" + " V",
            "cycle_count": "50000"
        }
        
        progress_callback.emit(current_state)
    
    def bistable_progress_update(self, current_state):
        '''
        Updates the gui for the bistable test
        '''
        
        print("bistable_progress_update function is called")
        self.bistable_grid_widget.button1_state.setText(current_state['button1_state'])
        self.bistable_grid_widget.button1_voltage.setText(current_state['button1_voltage'])
        self.bistable_grid_widget.cycle_count.setText(current_state['cycle_count'])

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

## to do list

# when test not running, update the background-colour of each grid
# think about adding the other signals for error, result and finished test