import pygame

pygame.init()

def init(): 
    pygame.init()
    win = pygame.display.set_mode((100,100))


def get_key(key_name):
    ans = False
    for eve in pygame.event.get():pass
    key_input = pygame.key.get_pressed()
    my_key = getattr(pygame, 'K_{}'.format(key_name))
    if key_input [my_key]:
        ans = True
        # print(f'{key_name} key was pressed')
    pygame.display.update()
    return ans

def main():
    if get_key('1'):
        return '1'
    if get_key('2'):
        return '2'



if __name__ == '__main__':
    init()
    while True:
        print(main())