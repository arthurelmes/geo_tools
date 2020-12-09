pro readgroundmeasurement_surfrad
  ;********************define the variable*******************************
  ;totapath='C:\Users\Angela.Erb\Dropbox\ValidationData\SURFRAD\' ;path for each site
  totapath='/ipswich/data02/arthur.elmes/in_situ/' ;path for each site
  sitepaname=['ft_peck/','dsrt_rk/','table_mnt/', 'sioux_fl/']
  sitename=['fpk','dra','tbl', 'sxf'] ;name of the site on each data file
  tdiff=[7.00,7.75,7.00,6.00]
  title=['month', 'day' ,'year' ,'gnd_mean' ,'gnd_sdev' ,'dir/dif_ratio' ,'diffuse/(dir+diff)','zen' ]

  for siteid = 0, 3 do begin
    for yid =2019, 2019 do begin
      year=yid
      print,year
      if year mod 4 eq 0 then daynum=366 else daynum=365
      ;********************define the variable*******************************
      month=intarr(1,daynum)
      dayout=intarr(1,daynum) ;Day in month
      dayname=strarr(1,daynum); DOY
      yeararr=intarr(1,daynum)
      gnd_mean=fltarr(1,daynum); 11:00-13:00
      gnd_sdev=fltarr(1,daynum)
      dir_dif_ratio=fltarr(1,daynum) ;
      skyl=fltarr(1,daynum); diffuse/(dir+diff)
      zen=fltarr(1,daynum);

      albedo11_1=fltarr(4)
      OUTDATA=STRARR(8,DAYNUM)

      ;*******************start a loop for sites***********************************
      print, totapath
      ;print, sitepaname(siteid)
      print, siteid
      sitepath=totapath+sitepaname(siteid)
      print, sitepath
      yearpath=string(year,format='(i04)')   ; path for the year, so if we have mutiply years we can do a for loop
      yearname=string(year mod 100,format='(i02)')  ; year in the file name
      ;************we can do a loop for days at here******************
      for dayi = 0, daynum-1 do begin

        dayname(dayi)=string(dayi+1,format='(i03)')
        fullname=sitepath+sitename(siteid)+yearname+dayname(dayi)+'.dat' ; the name for the file
        print, fullname
        ;file=sitename(siteid)+yearname+dayname(dayi)+'.dat'
        ft=FILE_TEST(fullname)
        if ft eq 1 then begin
          alldata=read_ascii(fullname,data_start=2)
          field01=alldata.field01
          dt=field01(6,*)-tdiff(siteid)
          ;*************read for 12********************
          id12=where(floor(dt*1000) eq 12000)
          month(dayi)=field01(2,id12)
          dayout(dayi)=field01(3,id12)
          yeararr(dayi)=field01(0,id12)

          ;**************read for 11-1* and 10:30-1:30****************************** HERE decide albedo at certain time
          id11_1=where(dt ge 11.01 and dt le 13.01)
          albedo11_1=calaveragep(field01,id11_1)
          gnd_mean(dayi)=albedo11_1(0)
          gnd_sdev(dayi)=albedo11_1(1)
          skyl(dayi)=albedo11_1(2)
          dir_dif_ratio(dayi)=albedo11_1(3)
          idzen=where(dt ge 10.8 and dt le 10.87)
          zen(dayi)=mean(field01(7,idzen));get the solar zenith angle
        endif

        ;***********************************************
      endfor ;endfor day
      OUTDATA(0,*)=string(month,format='(i02)')
      OUTDATA(1,*)=string(dayout,format='(i02)')
      OUTDATA(2,*)=string(yeararr,format='(i04)')
      OUTDATA(3,*)=string(gnd_mean,format='(f10.4)')
      OUTDATA(4,*)=string(gnd_sdev,format='(f10.4)')
      OUTDATA(5,*)=string(dir_dif_ratio,format='(f10.4)')
      OUTDATA(6,*)=string(skyl,format='(f10.4)')
      OUTDATA(7,*)=string(zen,format='(f10.4)')
      ;=[file,month, dayout ,yeararr ,gnd_mean ,gnd_sdev ,snow ,cfraction ,dir_dif_ratio , skyl]

      outname2=totapath+sitepaname(siteid)+string(year,format='(i04)')+'results.txt'
      openw,lun,outname2,/get_lun;
      printf,LUN,TITLE
      printf,lun,OUTDATA
      free_lun,lun

    endfor;end for yid

  endfor;end for site id

end
