#!/usr/bin/env lua

color=''
color0=''
color1=''
color2=''
color3=''

-- t = today
t = os.date('*t', os.time())

-- what day of the week to start the calendar on (e.g. 1 = Sunday, 2 = Monday, etc.)
start_dow = 2 -- Monday, as God intended
end_dow = (start_dow - 1 ) % 7 -- Sunday

-- e.g. how many days between today and Monday this wk
start_dow_this_week_offset = t.wday - start_dow

function add_remove_days(a_date, some_days)
   -- add or remove some days from a date and return the new date
   return os.date('*t', os.time{year=a_date.year, month=a_date.month, day=( a_date.day + some_days )})
end

start_date_this_wk = add_remove_days(t, -1 * start_dow_this_week_offset)
start_date = add_remove_days(start_date_this_wk, -7) -- start on Monday last week

end_date = add_remove_days(start_date, 7 * 9 - 1) -- show next 9 weeks including current

io.write('Mo Tu We Th Fr Sa Su\n')
month_name={ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' }

d = start_date
new_month = d.month

while os.time(d) <= os.time(end_date) do

   if d.year == t.year and d.month == t.month and d.day == t.day then
      io.write(color1)
   elseif os.time(d) < os.time(t) then
      io.write(color0)
   else
      if d.month == t.month then
         io.write(color)
      elseif (d.month - t.month) % 2 == 0 then
         io.write(color2)
      else
         io.write(color3)
      end
   end

   if d.day == 4 then
      new_month = d.month
   end
   
   io.write( string.format('%2d', d.day) .. ' ')

   if d.wday == end_dow then
      if new_month ~= '' then
         io.write(' ' .. color .. month_name[new_month]:upper())
         new_month = ''
      end
      
      io.write('\n')
   end

   d = add_remove_days(d, 1)
end

io.write(color)
