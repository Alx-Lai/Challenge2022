import pygame as pg

OBSTACLE_POSITION = [ \
	pg.Vector2(4.5,4.5), pg.Vector2(5.5,4.5), pg.Vector2(6.5,4.5), pg.Vector2(7.5,4.5),  \
	pg.Vector2(8.5,4.5), pg.Vector2(9.5,4.5), pg.Vector2(10.5,4.5), pg.Vector2(11.5,4.5),  \
	pg.Vector2(18.5,4.5), pg.Vector2(19.5,4.5), pg.Vector2(20.5,4.5), pg.Vector2(21.5,4.5),  \
	pg.Vector2(22.5,4.5), pg.Vector2(23.5,4.5), pg.Vector2(24.5,4.5), pg.Vector2(25.5,4.5),  \
	pg.Vector2(4.5,5.5), pg.Vector2(5.5,5.5), pg.Vector2(6.5,5.5), pg.Vector2(7.5,5.5),  \
	pg.Vector2(8.5,5.5), pg.Vector2(9.5,5.5), pg.Vector2(10.5,5.5), pg.Vector2(11.5,5.5),  \
	pg.Vector2(18.5,5.5), pg.Vector2(19.5,5.5), pg.Vector2(20.5,5.5), pg.Vector2(21.5,5.5),  \
	pg.Vector2(22.5,5.5), pg.Vector2(23.5,5.5), pg.Vector2(24.5,5.5), pg.Vector2(25.5,5.5),  \
	pg.Vector2(4.5,6.5), pg.Vector2(5.5,6.5), pg.Vector2(24.5,6.5), pg.Vector2(25.5,6.5),  \
	pg.Vector2(4.5,7.5), pg.Vector2(5.5,7.5), pg.Vector2(24.5,7.5), pg.Vector2(25.5,7.5),  \
	pg.Vector2(4.5,8.5), pg.Vector2(5.5,8.5), pg.Vector2(24.5,8.5), pg.Vector2(25.5,8.5),  \
	pg.Vector2(4.5,9.5), pg.Vector2(5.5,9.5), pg.Vector2(24.5,9.5), pg.Vector2(25.5,9.5),  \
	pg.Vector2(4.5,10.5), pg.Vector2(5.5,10.5), pg.Vector2(24.5,10.5), pg.Vector2(25.5,10.5),  \
	pg.Vector2(4.5,11.5), pg.Vector2(5.5,11.5), pg.Vector2(24.5,11.5), pg.Vector2(25.5,11.5),  \
	pg.Vector2(4.5,18.5), pg.Vector2(5.5,18.5), pg.Vector2(24.5,18.5), pg.Vector2(25.5,18.5),  \
	pg.Vector2(4.5,19.5), pg.Vector2(5.5,19.5), pg.Vector2(24.5,19.5), pg.Vector2(25.5,19.5),  \
	pg.Vector2(4.5,20.5), pg.Vector2(5.5,20.5), pg.Vector2(24.5,20.5), pg.Vector2(25.5,20.5),  \
	pg.Vector2(4.5,21.5), pg.Vector2(5.5,21.5), pg.Vector2(24.5,21.5), pg.Vector2(25.5,21.5),  \
	pg.Vector2(4.5,22.5), pg.Vector2(5.5,22.5), pg.Vector2(24.5,22.5), pg.Vector2(25.5,22.5),  \
	pg.Vector2(4.5,23.5), pg.Vector2(5.5,23.5), pg.Vector2(24.5,23.5), pg.Vector2(25.5,23.5),  \
	pg.Vector2(4.5,24.5), pg.Vector2(5.5,24.5), pg.Vector2(6.5,24.5), pg.Vector2(7.5,24.5),  \
	pg.Vector2(8.5,24.5), pg.Vector2(9.5,24.5), pg.Vector2(10.5,24.5), pg.Vector2(11.5,24.5),  \
	pg.Vector2(18.5,24.5), pg.Vector2(19.5,24.5), pg.Vector2(20.5,24.5), pg.Vector2(21.5,24.5),  \
	pg.Vector2(22.5,24.5), pg.Vector2(23.5,24.5), pg.Vector2(24.5,24.5), pg.Vector2(25.5,24.5),  \
	pg.Vector2(4.5,25.5), pg.Vector2(5.5,25.5), pg.Vector2(6.5,25.5), pg.Vector2(7.5,25.5),  \
	pg.Vector2(8.5,25.5), pg.Vector2(9.5,25.5), pg.Vector2(10.5,25.5), pg.Vector2(11.5,25.5),  \
	pg.Vector2(18.5,25.5), pg.Vector2(19.5,25.5), pg.Vector2(20.5,25.5), pg.Vector2(21.5,25.5),  \
	pg.Vector2(22.5,25.5), pg.Vector2(23.5,25.5), pg.Vector2(24.5,25.5), pg.Vector2(25.5,25.5)]
RE_FIELD_POSITION = [ \
	pg.Vector2(6.5,6.5), pg.Vector2(7.5,6.5), pg.Vector2(8.5,6.5), pg.Vector2(9.5,6.5),  \
	pg.Vector2(10.5,6.5), pg.Vector2(11.5,6.5), pg.Vector2(18.5,6.5), pg.Vector2(19.5,6.5),  \
	pg.Vector2(20.5,6.5), pg.Vector2(21.5,6.5), pg.Vector2(22.5,6.5), pg.Vector2(23.5,6.5),  \
	pg.Vector2(6.5,7.5), pg.Vector2(23.5,7.5), pg.Vector2(6.5,8.5), pg.Vector2(23.5,8.5),  \
	pg.Vector2(6.5,9.5), pg.Vector2(23.5,9.5), pg.Vector2(6.5,10.5), pg.Vector2(23.5,10.5),  \
	pg.Vector2(6.5,11.5), pg.Vector2(23.5,11.5), pg.Vector2(6.5,18.5), pg.Vector2(23.5,18.5),  \
	pg.Vector2(6.5,19.5), pg.Vector2(23.5,19.5), pg.Vector2(6.5,20.5), pg.Vector2(23.5,20.5),  \
	pg.Vector2(6.5,21.5), pg.Vector2(23.5,21.5), pg.Vector2(6.5,22.5), pg.Vector2(23.5,22.5),  \
	pg.Vector2(6.5,23.5), pg.Vector2(7.5,23.5), pg.Vector2(8.5,23.5), pg.Vector2(9.5,23.5),  \
	pg.Vector2(10.5,23.5), pg.Vector2(11.5,23.5), pg.Vector2(18.5,23.5), pg.Vector2(19.5,23.5),  \
	pg.Vector2(20.5,23.5), pg.Vector2(21.5,23.5), pg.Vector2(22.5,23.5), pg.Vector2(23.5,23.5)]
