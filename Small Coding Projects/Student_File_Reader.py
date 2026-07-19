# Implementation of the StudentFileReader ADT using a text file as the
# input source in which each field is stored on a separate line.

class StudentFileReader :
    # Create a new student reader instance.
    def __init__( self, inputSrc ):
        self._inputSrc = inputSrc
        self._inputFile = None

    # Open a connection to the input file.
    def open( self ):
        self._inputFile = open( self._inputSrc, "r" )

    # Close the connection to the input file.
    def close( self ):
        self._inputFile.close()
        self._inputFile = None

    # Extract all student records and store them in a list.
    def fetchAll( self ):
        theRecords = list()
        student = self.fetchRecord()
        while student != None :
            theRecords.append( student )
            student = self.fetchRecord()
        return theRecords


    '''This is for fetching data in the format:
    102535
    Wan
    Daniel 
    [0,1,2,3]  # representing student level
    3.85  # float as gpa'''
    # Extract the next student record from the file.
    def fetchRecord( self ):
        # Read the first line of the record.
        line = self._inputFile.readline()
        if line == "" :
            return None

        # If there is another record, create a storage object and fill it.
        student = StudentRecord()
        student.idNum = int( line )
        student.firstName = self._inputFile.readline().rstrip()
        student.lastName = self._inputFile.readline().rstrip()
        student.classCode = int( self._inputFile.readline() )
        student.gpa = float( self._inputFile.readline() )
        return student


    '''This is designed for the format:
    10015, John, Smith, 2, 3.01
    10334, Jane, Roberts, 4, 3.81
    10208, Patrick, Green, 1, 3.95'''
    def fetchRecord_2(self):
        line = self._inputFile.readline()

        if line == '':
            return None

        # Split the line into a list of parts based on the commas
        parts = line.split(',')

        student = StudentRecord()
        
        # Access the fields by their index in the 'parts' list
        student.idNum = int(parts[0])
        student.firstName = parts[1].strip()
        student.lastName = parts[2].strip()
        student.classCode = int(parts[3])
        student.gpa = float(parts[4])
        
        return student
            

            


# Storage class used for an individual student record.
class StudentRecord :
    def __init__( self ):
        self.idNum = 0
        self.firstName = None
        self.lastName = None
        self.classCode = 0
        self.gpa = 0.0


        


