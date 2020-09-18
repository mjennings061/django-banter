import matlab.engine


def run_file(file_path):
    # eng = matlab.engine.start_matlab()    # start a new MATLAB session
    eng = matlab.engine.connect_matlab()    # connect to an open MATLAB window
    eng.addpath(r'C:\Users\MJ\OneDrive - Ulster University\Documents\PhD\Django\django-banter\ecg\media\algorithm',
                nargout=0)
    eng.LPF_single_row(file_path, nargout=1)
    eng.quit()

# file_path = 'C:/Users/MJ/OneDrive - Ulster University/Documents/PhD/Django/django-banter/ecg/media' \
#                     '/mj_6c493203-13fa-482f-a815-5821a9ed29c3.csv '
