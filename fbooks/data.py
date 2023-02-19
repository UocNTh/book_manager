
def get_data(object , dict ) :  
    # Danh sach cac thuoc tinh va gia tri cua mot class
    atts = vars(object)
    for att in atts : 
        if not att.startswith('_') :  
            dict[att] = atts[att] 

