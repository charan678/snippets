def utc_local_time(dateinfo, local_zone_name=None, indateformat="%d-%b-%Y %H:%M:%S", outdateformat=None, outstring=False):
    '''
    @summary: convert dateinfo from utc to program timezone
    @params: dateinfo: date time can be in string format or datetime object
    @params: time_zone_name: timezone to convert to
    @params: indateformat: if dateinfo is in string format then user can define in date format, by default indateformat is "%d-%b-%Y %H:%M:%S"
    @params: outdateformat:if dateinfo is in string format then user can define out date format. if out date format is not define then outdatefromat
             is equal to indateformat
    '''
    if not dateinfo:
        return None
    
    dateobj = None
    if not outdateformat:
        outdateformat = indateformat
    
    if type(dateinfo) == str or type(dateinfo) == unicode:
        dateinfo = datetime.datetime.strptime(dateinfo,indateformat)
    if local_zone_name:
        temp_date = dateinfo.replace(tzinfo=pytz.utc)
        temp_zone = pytz.timezone(local_zone_name)
        zone_date = temp_date.astimezone(temp_zone)
        #Django template some problem with timezone's
        dateobj = zone_date.replace(tzinfo=None)
        if outstring:
            dateobj = dateobj.strftime(outdateformat)
    else:
        if outstring:
            dateobj = dateinfo.strftime(outdateformat)
    return dateobj

def local_utc_time(dateinfo,local_zone_name=None,indateformat="%d-%b-%Y %H:%M:%S",outdateformat=None,outstring=False):
    '''
    @summary: convert dateinfo from program timezone to utc zone dateinfo
    @params: dateinfo: date time can be in string format or datetime object
    @params: local_zone_name: timezone to convert from
    @params: indateformat: if dateinfo is in string format then user can define in date format, by default indateformat is "%d-%b-%Y %H:%M:%S"
    @params: outdateformat:if dateinfo is in string format then user can define out date format. if out date format is not define then outdatefromat
             is equal to indateformat
    '''
    if not dateinfo:
        return None
    dateobj = None
    if not outdateformat:
        outdateformat = indateformat
    if local_zone_name:
        if type(dateinfo) == str or type(dateinfo) == unicode:
            dateinfo = datetime.datetime.strptime(dateinfo,indateformat)
        from_zone = pytz.timezone(local_zone_name)
        to_zone = pytz.utc
        local_time = from_zone.localize(dateinfo)
        dateobj = local_time.astimezone(to_zone)
        dateobj = dateobj.replace(tzinfo=pytz.utc)
        if outstring:
            dateobj = dateobj.strftime(outdateformat)
    else:
        if type(dateinfo) == str or type(dateinfo) == unicode:
            dateinfo = parser.parse(dateinfo)
            if dateinfo.tzinfo == None:
                raise ValidationError("Datetime input doesnot contain timezone info")
            to_zone = pytz.utc
            dateobj = dateinfo.astimezone(to_zone)
            dateobj = dateobj.strftime(outdateformat)
        else:
            if dateinfo.tzinfo == None:
                raise ValidationError("Datetime input doesnot contain timezone info")
            to_zone = pytz.utc
            dateobj = dateinfo.astimezone(to_zone)
            if outstring:
                dateobj = dateobj.strftime(outdateformat)
    return dateobj

