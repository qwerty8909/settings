:: пути к папкам источникам
set fr_a=d:\xxx\Chain\Elena
set fr_b=d:\xxx\Sdi\Elena
set fr_c=d:\xxx\Dis\Elena
set fr_d=d:\xxx\Pat\Elena

:: пути к папкам назначения
set to_a=d:\yyy\%date:~-10%\Chain\Elena
set to_b=d:\yyy\%date:~-10%\Sdi\Elena
set to_c=d:\yyy\%date:~-10%\Dis\Elena
set to_d=d:\yyy\%date:~-10%\Pat\Elena

md "%to_a%"
md "%to_b%"
md "%to_c%"
md "%to_d%"
xcopy /s "%fr_a%\" "%to_a%"
xcopy /s "%fr_b%\" "%to_b%"
xcopy /s "%fr_c%\" "%to_c%"
xcopy /s "%fr_d%\" "%to_d%"