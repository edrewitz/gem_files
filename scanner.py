def gem_global_scanner(final_forecast_hour, proxies):
    
    """
    This function scans https://dd.weather.gc.ca/ for the file with the latest GEM Global run. 
    
    If the page has complete data, the download link will be returned. 
    If the page is incomplete, the scanner will check for the previous run data.  
    
    Required Arguments:
    
    1) final_forecast_hour (Integer) - Default = 240. The final forecast hour the user wishes to download. The GEM Global
    goes out to 240 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    2) proxies (dict or None) - If the user is using a proxy server, the user must change the following:

    proxies=None ---> proxies={'http':'http://url',
                            'https':'https://url'
                        }
    
    Optional Arguments: None
    
                        
    Returns
    -------

    1) The download link.
    2) The time of the latest model run. 
    3) The date of the run in the form of a string
    """
    
    if final_forecast_hour < 10:
        final_forecast_hour = f"00{final_forecast_hour}"
    elif final_forecast_hour >= 10 and final_forecast_hour < 100:
        final_forecast_hour = f"0{final_forecast_hour}"
    else:
        final_forecast_hour = f"{final_forecast_hour}"
        
    
    f_today_00z = f"CMC_glb_ABSV_ISBL_200_latlon.15x.15_{now.strftime('%Y%m%d')}00_P{final_forecast_hour}.grib2"
    f_today_12z = f"CMC_glb_ABSV_ISBL_200_latlon.15x.15_{now.strftime('%Y%m%d')}12_P{final_forecast_hour}.grib2"
    f_yday_00z = f"CMC_glb_ABSV_ISBL_200_latlon.15x.15_{yd.strftime('%Y%m%d')}00_P{final_forecast_hour}.grib2"
    f_yday_12z = f"CMC_glb_ABSV_ISBL_200_latlon.15x.15_{yd.strftime('%Y%m%d')}12_P{final_forecast_hour}.grib2"

    
    url_today_00z = f"https://dd.weather.gc.ca/{now.strftime('%Y%m%d')}/WXO-DD/model_gem_global/15km/grib2/lat_lon/00/{final_forecast_hour}/"
    url_today_12z = f"https://dd.weather.gc.ca/{now.strftime('%Y%m%d')}/WXO-DD/model_gem_global/15km/grib2/lat_lon/12/{final_forecast_hour}/"
    url_yday_00z = f"https://dd.weather.gc.ca/{yd.strftime('%Y%m%d')}/WXO-DD/model_gem_global/15km/grib2/lat_lon/00/{final_forecast_hour}/"
    url_yday_12z = f"https://dd.weather.gc.ca/{yd.strftime('%Y%m%d')}/WXO-DD/model_gem_global/15km/grib2/lat_lon/12/{final_forecast_hour}/"
    
    download_url_t_00z = f"https://dd.weather.gc.ca/{now.strftime('%Y%m%d')}/WXO-DD/model_gem_global/15km/grib2/lat_lon/00/"
    download_url_t_12z = f"https://dd.weather.gc.ca/{now.strftime('%Y%m%d')}/WXO-DD/model_gem_global/15km/grib2/lat_lon/12/"
    download_url_y_00z = f"https://dd.weather.gc.ca/{yd.strftime('%Y%m%d')}/WXO-DD/model_gem_global/15km/grib2/lat_lon/00/"
    download_url_y_12z = f"https://dd.weather.gc.ca/{yd.strftime('%Y%m%d')}/WXO-DD/model_gem_global/15km/grib2/lat_lon/12/"
    
    if proxies == None:
        t_12z = requests.get(f"{url_today_12z}/{f_today_12z}", stream=True)
        t_00z = requests.get(f"{url_today_00z}/{f_today_00z}", stream=True)
        y_12z = requests.get(f"{url_yday_12z}/{f_yday_12z}", stream=True)
        y_00z = requests.get(f"{url_yday_00z}/{f_yday_00z}", stream=True)
    else:
        t_12z = requests.get(f"{url_today_12z}/{f_today_12z}", stream=True, proxies=proxies)
        t_00z = requests.get(f"{url_today_00z}/{f_today_00z}", stream=True, proxies=proxies)
        y_12z = requests.get(f"{url_yday_12z}/{f_yday_12z}", stream=True, proxies=proxies)
        y_00z = requests.get(f"{url_yday_00z}/{f_yday_00z}", stream=True, proxies=proxies)       
    
    if t_12z.status_code == 200:
        url = download_url_t_12z
        run = '12'
        date =f"{now.strftime('%Y%m%d')}"
    elif t_12z.status_code != 200 and t_00z.status_code == 200:
        url = download_url_t_00z
        run = '00'        
        date =f"{now.strftime('%Y%m%d')}"
    elif t_12z.status_code != 200 and t_00z.status_code != 200 and y_12z.status_code == 200:
        url = download_url_y_12z
        run = '12'
        date =f"{yd.strftime('%Y%m%d')}"
    else:
        url = download_url_y_00z
        run = '00'
        date =f"{yd.strftime('%Y%m%d')}"
        
    return url, run, date
    

