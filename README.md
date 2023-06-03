# Process_mining

Installing required packages:

following needs to be installed:

pmp4py: https://pypi.org/project/pm4py/
reactiveX: https://reactivex.io/
pybeamline: https://beamline.cloud/pybeamline/

They can all be installed by pip
for pybeamline use: pip install -i https://test.pypi.org/simple/ pybeamline

install Graphviz

pip might not work for this, instead install directly to website: https://pygraphviz.github.io/
graphviz\bin is required to be added to your system PATH.


Your first program:

check out reactivex https://rxpy.readthedocs.io/en/latest/index.html for guidelines on how the variable type observable works.
or it is possible from pybeamline.source to use xes_log_source_from_file. Which converts an .XES file into a type observable.

Initiate an object from a class from either the 2 process mining files: Process_Discovery.py, Conformance_Checking.py.
Configure the object with the respective class' method.
call subscribe which takes type observable as input.


example:

source = xes_log_source_from_file("XES-files\HM_LC-test.xes")

new_HM_LC = Process_Discovery.HM_LC(max_approx_error=0.05, dependency_threshold=0, and_threshold=0.8)
new_HM_LC.setModelRefreshRate(8) #by default is 1/max_approx_error
new_HM_LC.setLabel('Dependency') #by default is Frequency
new_HM_LC.setFileName('test')
new_HM_LC.subscribe(source)

