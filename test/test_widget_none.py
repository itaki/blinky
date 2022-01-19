"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - NONE
Test NoneWidget, HMargin, VMargin and MenuLink widgets.
"""

__all__ = ['NoneWidgetTest']

from test._utils import MenuUtils, surface, PygameEventUtils, BaseTest

import pygame_menu
import pygame_menu.controls as ctrl

from pygame_menu.widgets import NoneWidget, NoneSelection
from pygame_menu.widgets.core.widget import WidgetTransformationNotImplemented


class NoneWidgetTest(BaseTest):

    def test_none(self) -> None:
        """
        Test none widget.
        """
        wid = NoneWidget()

        wid.set_margin(9, 9)
        self.assertEqual(wid.get_margin(), (0, 0))

        wid.set_padding(9)
        self.assertEqual(wid.get_padding(), (0, 0, 0, 0))

        wid.set_background_color((1, 1, 1))
        wid._draw_background_color(surface)
        self.assertIsNone(wid._background_color)

        no_sel = NoneSelection()
        wid.set_selection_effect(no_sel)
        self.assertNotEqual(no_sel, wid.get_selection_effect())

        wid.set_title('none')
        self.assertEqual(wid.get_title(), '')

        r = wid.get_rect(inflate=(10, 10))
        self.assertEqual(r.x, 0)
        self.assertEqual(r.y, 0)
        self.assertEqual(r.width, 0)
        self.assertEqual(r.height, 0)

        self.assertFalse(wid.is_selectable)
        self.assertTrue(wid.is_visible())

        wid.apply()
        wid.change()

        # noinspection SpellCheckingInspection
        wid.set_font('myfont', 0, (1, 1, 1), (1, 1, 1), (1, 1, 1), (0, 0, 0), (0, 0, 0))
        wid.update_font({'name': ''})
        wid._apply_font()
        self.assertIsNone(wid._font)

        # Test font rendering
        surf = wid._render_string('nice', (1, 1, 1))
        self.assertEqual(surf.get_width(), 0)
        self.assertEqual(surf.get_height(), 0)

        wid._apply_transforms()

        wid.hide()
        self.assertFalse(wid.is_visible())
        wid.show()
        self.assertTrue(wid.is_visible())

        self.assertRaises(ValueError, lambda: wid.get_value())

        surf = wid.get_surface()
        self.assertEqual(surf.get_width(), 0)
        self.assertEqual(surf.get_height(), 0)

        # Apply transforms
        wid.set_position(1, 1)
        self.assertEqual(wid.get_position(), (0, 0))

        self.assertRaises(WidgetTransformationNotImplemented, lambda: wid.translate(1, 1))
        self.assertEqual(wid.get_translate(), (0, 0))

        self.assertRaises(WidgetTransformationNotImplemented, lambda: wid.rotate(10))
        self.assertEqual(wid._angle, 0)

        self.assertRaises(WidgetTransformationNotImplemented, lambda: wid.resize(10, 10))
        self.assertFalse(wid._scale[0])
        self.assertEqual(wid._scale[1], 1)
        self.assertEqual(wid._scale[2], 1)

        self.assertRaises(WidgetTransformationNotImplemented, lambda: wid.scale(100, 100))
        self.assertFalse(wid._scale[0])
        self.assertEqual(wid._scale[1], 1)
        self.assertEqual(wid._scale[2], 1)

        self.assertRaises(WidgetTransformationNotImplemented, lambda: wid.flip(True, True))
        self.assertFalse(wid._flip[0])
        self.assertFalse(wid._flip[1])

        self.assertRaises(WidgetTransformationNotImplemented, lambda: wid.set_max_width(100))
        self.assertIsNone(wid._max_width[0])

        self.assertRaises(WidgetTransformationNotImplemented, lambda: wid.set_max_height(100))
        self.assertIsNone(wid._max_height[0])

        # Selection
        wid.select()
        self.assertFalse(wid.is_selected())
        self.assertFalse(wid.is_selectable)

        # noinspection PyTypeChecker
        wid.set_sound(None)
        self.assertIsNotNone(wid._sound)

        wid.set_border(1, (0, 0, 0), (0, 0))
        self.assertEqual(wid._border_width, 0)
        self.assertEqual(wid.get_selected_time(), 0)

        # Test events
        def my_event() -> None:
            """
            Generic event object.
            """
            return

        wid.set_onchange(my_event)
        self.assertIsNone(wid._onchange)
        wid.set_onmouseover(my_event)
        self.assertIsNone(wid._onmouseover)
        wid.set_onmouseleave(my_event)
        self.assertIsNone(wid._onmouseleave)
        wid.set_onselect(my_event)
        self.assertIsNone(wid._onselect)
        wid.set_onreturn(my_event)
        self.assertIsNone(wid._onreturn)
        wid.mouseleave()
        wid.mouseover()
        wid._mouseover = True
        wid._check_mouseover()
        self.assertFalse(wid._mouseover)

    def test_draw_update(self) -> None:
        """
        Test draw and update callbacks.
        """
        wid = NoneWidget()

        # Test draw update
        draw = [False]

        # noinspection PyUnusedLocal
        def _draw(*args) -> None:
            draw[0] = True

        draw_id = wid.add_draw_callback(_draw)
        self.assertIsInstance(draw_id, str)
        wid.draw(surface)
        self.assertTrue(draw[0])
        draw[0] = False
        wid.remove_draw_callback(draw_id)
        self.assertRaises(IndexError, lambda: wid.remove_draw_callback(draw_id))
        wid.draw(surface)
        self.assertFalse(draw[0])

        # Test update
        update = [False]

        # noinspection PyUnusedLocal
        def _update(*args) -> None:
            update[0] = True

        update_id = wid.add_update_callback(_update)
        self.assertIsInstance(update_id, str)
        self.assertFalse(wid.update(surface))
        self.assertTrue(update[0])
        update[0] = False
        wid.remove_update_callback(update_id)
        self.assertRaises(IndexError, lambda: wid.remove_update_callback(update_id))
        wid.update(surface)
        self.assertFalse(update[0])

    def test_hmargin(self) -> None:
        """
        Test horizontal margin widget.
        """
        w = pygame_menu.widgets.HMargin(999)
        w._render()
        self.assertEqual(w.get_rect().width, 999)
        self.assertEqual(w.get_rect().height, 0)
        self.assertFalse(w.update([]))
        self.assertEqual(w._font_size, 0)
        self.assertEqual(w.get_margin(), (0, 0))
        w.draw(surface)

        menu = MenuUtils.generic_menu()
        w = menu.add._horizontal_margin(999)
        self.assertEqual(w.get_rect().width, 999)
        self.assertEqual(w.get_rect().height, 0)

    def test_vmargin(self) -> None:
        """
        Test vertical margin widget.
        """
        menu = MenuUtils.generic_menu()
        w = menu.add.vertical_margin(999)
        w._render()
        self.assertEqual(w.get_rect().width, 0)
        self.assertEqual(w.get_rect().height, 999)
        self.assertFalse(w.update([]))
        self.assertEqual(w._font_size, 0)
        self.assertEqual(w.get_margin(), (0, 0))
        w.draw(surface)

    # noinspection PyTypeChecker
    def test_menu_link(self) -> None:
        """
        Test menu link.
        """
        menu = MenuUtils.generic_menu()
        menu1 = MenuUtils.generic_menu(title='Menu1', theme=pygame_menu.themes.THEME_BLUE)
        menu1.add.button('Back', pygame_menu.events.BACK)
        menu2 = MenuUtils.generic_menu(title='Menu2', theme=pygame_menu.themes.THEME_ORANGE)
        menu2.add.button('Back', pygame_menu.events.BACK)
        menu3 = MenuUtils.generic_menu(title='Menu3', theme=pygame_menu.themes.THEME_GREEN)
        menu3.add.button('Back', pygame_menu.events.BACK)
        btn1 = menu.add.button('menu1', menu1)
        btn2 = menu.add.button('menu2', menu2)
        btn3 = menu.add.button('menu3', menu3)

        # Hide the buttons
        btn1.hide()
        btn2.hide()
        btn3.hide()

        # Now open menu with the button, this should open Menu1 by default
        self.assertEqual(menu.get_current(), menu)
        btn1.apply()
        self.assertEqual(menu.get_current(), menu1)
        menu.full_reset()
        self.assertEqual(menu.get_current(), menu)

        # Add menu link
        link_test = menu.add.menu_link(menu2)
        link_test.open()
        self.assertEqual(menu.get_current(), menu2)
        menu.full_reset()
        self.assertEqual(menu.get_current(), menu)

        self.assertFalse(link_test.is_visible())
        link_test.hide()
        self.assertFalse(link_test.is_visible())
        link_test.show()
        self.assertFalse(link_test.is_visible())

        self.assertRaises(ValueError, lambda: menu.add.menu_link(menu))

        # Invalid objects
        self.assertRaises(ValueError, lambda: menu.add.menu_link(True))

        # noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring
        def open_link(*args) -> None:
            link: 'pygame_menu.widgets.MenuLink' = args[-1]
            self.assertIsInstance(link, pygame_menu.widgets.MenuLink)
            link.open()

        # Add a selection object, which opens the links
        sel = menu.add.selector('Change menu ', [
            ('Menu 1', menu.add.menu_link(menu1)),
            ('Menu 2', menu.add.menu_link(menu2)),
            ('Menu 3', menu.add.menu_link(menu3))
        ], onreturn=open_link, style=pygame_menu.widgets.SELECTOR_STYLE_FANCY)

        sel.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))

    def test_value(self) -> None:
        """
        Test value.
        """
        menu = MenuUtils.generic_menu()
        menu2 = MenuUtils.generic_menu()
        widgets = [
            menu.add.none_widget(),
            menu.add.vertical_margin(1),
            menu.add._horizontal_margin(1),
            menu.add.menu_link(menu2)
        ]
        for w in widgets:
            self.assertRaises(ValueError, lambda: w.get_value())
            self.assertRaises(ValueError, lambda: w.set_value('value'))
            self.assertRaises(ValueError, lambda: w.set_default_value('value'))
            self.assertFalse(w.value_changed())
            w.reset_value()

    def test_shadow(self) -> None:
        """
        Test shadow.
        """
        menu = MenuUtils.generic_menu()
        w = menu.add.vertical_margin(1)
        w.shadow(10, 10)
        self.assertFalse(w._shadow['enabled'])
