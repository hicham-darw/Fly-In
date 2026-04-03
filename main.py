import pyglet

window = pyglet.window.Window()
window.set_size(5000, 3000)
image = pyglet.resource.image('hel-hamo.jpg')
###
    #
        /#
@window.event
def on_draw():
    window.clear()
    image.blit(0, 0)

pyglet.app.run()
