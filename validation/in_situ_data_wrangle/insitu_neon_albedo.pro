pro insitu_NEON_albedo

  ;indir='C:\Users\Angela.Erb\Dropbox\ValidationData\NEON-30-extract\Tminus7\*.csv'
  indir='C:\Users\Angela.Erb\Dropbox\ValidationData\NEON\rad-net\rn-minus9\m9-2019\*Z.csv'


  print, indir
  sitename = FILE_SEARCH(indir); find the input file in the path
  print, sitename
  sitenum=N_ELEMENTS(sitename) ;how many files
  title=['year','DOY'  ,'gnd_mean' ,'gnd_sdev' ]

  for siteid = 0, sitenum-1 do begin

    fullname=sitename(siteid) ; the name for the file
    print, fullname
    
    ft=FILE_TEST(fullname)
    if ft eq 1 then begin;file check
      alldata= READ_CSV(fullname,  HEADER=SedHeader)
      DATE=alldata.field01;start time, end is in next 30min
      insw=float(alldata.field03)
      insw_qa=float(alldata.field10); 0 is good, 1 is bad
      outsw=float(alldata.field11)
      outsw_qa=float(alldata.field34); 0 is good, 1 is bad
      qa_all=insw_qa+outsw_qa; 0 is good, 1 is bad
      YEAR=strmid(DATE,0,4)
      month=strmid(DATE,5,2)
      DAY=strmid(DATE,8,2)
      HOUR=strmid(DATE,11,2)
      MINI=strmid(DATE,14,2)
      DOY=JULDAY(MONTH,DAY,YEAR)-JULDAY(1,1,2019)+1;Base on 2019
      dt=HOUR+mini/60-9;change for sites
      albedo=outsw/insw
      startday=min(DOY)
      endday=max(DOY)
      OUTDATA=STRARR(4,endday-startday+1)
      dayout=intarr(1,endday-startday+1)
      gnd_mean=fltarr(1,endday-startday+1); 11:00-13:00
      gnd_sdev=fltarr(1,endday-startday+1)
      for dayi=0, endday-startday do begin
        albedo_d=0
        qa_all_d=0
        dt_d=0
        if mean(where(DOY eq dayi+startday)) ge 0 then begin
        albedo_d=albedo(where(DOY eq dayi+startday));
        qa_all_d=qa_all(where(DOY eq dayi+startday))
        dt_d=dt(where(DOY eq dayi+startday))   
        endif     
        dayout(dayi)=dayi+startday

        ;************** read for 11-1 *******************************
        id11_1=where((dt_d ge 10.00) and (dt lt 11.00) and (qa_all_d eq 0))
        if mean(id11_1) ge 0 then albedo_noon=albedo_d(id11_1) else albedo_noon=0
        gnd_mean(dayi)=mean(albedo_noon)
        gnd_sdev(dayi)=stddev(albedo_noon)
        
      endfor; endfor days
      
      OUTDATA(0,*)=string(2019,format='(i04)')
      OUTDATA(1,*)=string(dayout,format='(i03)')
      OUTDATA(2,*)=string(gnd_mean,format='(f10.4)')
      OUTDATA(3,*)=string(gnd_sdev,format='(f10.4)')
      
      name_len=strlen(fullname)
      File_IN_r=strmid(fullname,0,name_len-4)
      outname2=File_IN_r+'albedo.txt'
      print,outname2
      openw,lun,outname2,/get_lun;
      printf,LUN,TITLE
      printf,lun,OUTDATA
      free_lun,lun

    END
  END
end
