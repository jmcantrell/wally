import os.path
import gtk, pygtk; pygtk.require('2.0')

from pkg_resources import Requirement, resource_filename

from imageutils.color import rgb8_to_rgb16, rgb16_to_rgb8
from pathutils import condense
from gnomeutils import Thumbnails
from gtkutils import get_icon_list
from gtkutils import AboutDialog, StandardDialog, DirectoryChooserDialog
from gtkutils.treeview import column_text

from . import Wally
from . import WALLPAPER_TYPES
from . import __appname__, __author__, __url__, __license__

def get_resource(name): #{{{1
    return resource_filename(
            Requirement.parse(__appname__),
            os.path.join(__appname__.lower(), name)
            )

def get_icon(name): #{{{1
    return get_resource(os.path.join('icons', name))

def main(opts, args): #{{{1
    w = WallyGTK()
    gtk.main()

#}}}1

class ExclusionsDialog(StandardDialog): #{{{1

    COL_EX = 0

    def __init__(self, exclusions, **kwargs):
        super(ExclusionsDialog, self).__init__(**kwargs)
        self.set_title('Exclusions')
        self.set_default_size(400, 300)
        self.treeview = gtk.TreeView(gtk.ListStore(str))
        self.treeview.set_headers_visible(False)
        self.treeview.append_column(column_text('Exclusion', self.COL_EX))
        self.treeview.connect('cursor-changed', self.on_treeview_cursor_changed)
        scrolled = gtk.ScrolledWindow()
        scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled.add_with_viewport(self.treeview)
        add_box = gtk.HBox()
        self.add_entry = gtk.Entry()
        self.add_entry.connect('changed', self.on_add_entry_changed)
        add_box.pack_start(self.add_entry)
        self.add_button = gtk.Button('Add')
        self.add_button.set_image(gtk.image_new_from_stock(gtk.STOCK_ADD, gtk.ICON_SIZE_MENU))
        self.add_button.connect('clicked', self.on_add_button_clicked)
        self.add_entry.connect_object('activate', gtk.Button.clicked, self.add_button)
        add_box.pack_start(self.add_button, fill=False, expand=False)
        self.remove_button = gtk.Button(stock=gtk.STOCK_REMOVE)
        self.remove_button.connect('clicked', self.on_remove_button_clicked)
        self.remove_button.set_sensitive(False)
        self.vbox.pack_start(add_box, fill=False, expand=False)
        self.vbox.pack_start(scrolled)
        self.vbox.pack_start(self.remove_button, fill=False, expand=False)
        self.set_exclusions(exclusions)

    def add_exclusion(self, exclusion):
        self.treeview.get_model().append([exclusion])

    def set_exclusions(self, exclusions):
        self.treeview.get_model().clear()
        for ex in exclusions: self.add_exclusion(ex)

    def get_exclusions(self):
        return [row[self.COL_EX] for row in self.treeview.get_model()]

    def on_add_button_clicked(self, widget):
        exclusion = self.add_entry.get_text()
        if not exclusion: return
        self.add_exclusion(exclusion)

    def on_remove_button_clicked(self, widget):
        model, itr = self.treeview.get_selection().get_selected()
        path = model.get_path(itr)
        del(model[path])
        self.remove_button.set_sensitive(False)

    def on_treeview_cursor_changed(self, widget):
        self.remove_button.set_sensitive(True)

    def on_add_entry_changed(self, entry):
        if len(entry.get_text().strip()):
            self.add_button.set_sensitive(True)
        else:
            self.add_button.set_sensitive(False)



class BackgroundColorDialog(gtk.ColorSelectionDialog): #{{{1

    def __init__(self, color):
        super(BackgroundColorDialog, self).__init__(title='Background Color')
        self.colorsel.set_current_color(color)

    def run(self):
        r = super(BackgroundColorDialog, self).run()
        if r != gtk.RESPONSE_OK:
            color = None
        else:
            color = self.colorsel.get_current_color()
        self.hide()
        return color



class DirectoriesDialog(StandardDialog): #{{{1

    def __init__(self, directories, **kwargs):
        super(DirectoriesDialog, self).__init__(**kwargs)
        self.set_title('Directories')
        self.notebook = gtk.Notebook()
        self.vbox.add(self.notebook)
        self.set_directories(directories)

    def clear_pages(self):
        for n in range(self.notebook.get_n_pages()):
            self.notebook.remove_page(n)

    def set_directories(self, directories):
        self.clear_pages()
        self.pages = {}
        for wt, dirs in directories.iteritems():
            page = DirectoriesPage(dirs)
            self.pages[wt] = page
            self.notebook.append_page(page, gtk.Label(wt.title()))

    def get_directories(self):
        directories = {}
        for wt, page in self.pages.iteritems():
            directories[wt] = page.get_directories()
        return directories



class DirectoriesPage(gtk.Frame): #{{{1

    COL_DIR = 0

    def __init__(self, directories):
        super(DirectoriesPage, self).__init__()
        self.treeview = gtk.TreeView(gtk.ListStore(str))
        self.treeview.set_headers_visible(False)
        self.treeview.append_column(column_text('Directory', self.COL_DIR))
        self.treeview.connect('cursor-changed', self.on_treeview_cursor_changed)
        scrolled = gtk.ScrolledWindow()
        scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled.add_with_viewport(self.treeview)
        self.add_button = gtk.Button(stock=gtk.STOCK_ADD)
        self.add_button.connect('clicked', self.on_add_button_clicked)
        self.remove_button = gtk.Button(stock=gtk.STOCK_REMOVE)
        self.remove_button.connect('clicked', self.on_remove_button_clicked)
        self.remove_button.set_sensitive(False)
        bbox = gtk.HButtonBox()
        bbox.set_layout(gtk.BUTTONBOX_SPREAD)
        bbox.add(self.add_button)
        bbox.add(self.remove_button)
        vbox = gtk.VBox()
        vbox.pack_start(scrolled)
        vbox.pack_start(bbox, fill=False, expand=False)
        self.add(vbox)
        self.set_directories(directories)

    def add_directory(self, directory):
        self.treeview.get_model().append([condense(directory)])

    def set_directories(self, directories):
        self.treeview.get_model().clear()
        for d in directories: self.add_directory(d)

    def get_directories(self):
        model = self.treeview.get_model()
        return [os.path.expanduser(row[self.COL_DIR]) for row in model]

    def on_add_button_clicked(self, widget):
        directory = DirectoryChooserDialog().run()
        if not directory: return
        self.add_directory(directory)

    def on_remove_button_clicked(self, widget):
        model, itr = self.treeview.get_selection().get_selected()
        path = model.get_path(itr)
        del(model[path])
        self.remove_button.set_sensitive(False)

    def on_treeview_cursor_changed(self, widget):
        self.remove_button.set_sensitive(True)


class WallpaperIconView(gtk.IconView): #{{{1

    COL_FILE, COL_PIX = range(2)

    def __init__(self, app, **kwargs):
        super(WallpaperIconView, self).__init__(**kwargs)
        self.app = app
        self.set_model(gtk.ListStore(str, gtk.gdk.Pixbuf))
        self.set_pixbuf_column(self.COL_PIX)
        self.set_tooltip_column(self.COL_FILE)

    def set_wallpapers(self, wallpapers):
        model = self.get_model()
        model.clear()
        for w in wallpapers:
            model.append([w, self.app.get_thumbnail(w)])

    def get_selected(self):
        model = self.get_model()
        items = self.get_selected_items()
        if not items: return None
        return model[items[0]][self.COL_FILE]

    def clear(self):
        self.get_model().clear()



class MainWindow(gtk.Window): #{{{1

    def __init__(self, app):
        super(MainWindow, self).__init__(gtk.WINDOW_TOPLEVEL)
        self.set_icon_list(*get_icon_list(get_icon('logo.svg')))
        self.set_default_size(600, 500)
        self.app = app
        self.set_title(__appname__)
        self.add(self._get_window_content())
        self.show_all()

    def refresh_wallpapers(self, query=None):
        del(self.app.wally.searches)
        if query: self.app.wally.searches = [query]
        self.app.wally.refresh_wallpapers()
        dt = self.app.wally.display_type[self.displays.get_active()]
        wallpapers = [w[1] for w in sorted(
            ((os.path.getmtime(w), w) for w in self.app.wally.wallpapers.get(dt, [])),
            reverse=True)[:int(self.search_limit.get_value())]]
        self.wallpaper_view.set_wallpapers(wallpapers)
        self.update_wallpaper_count(len(wallpapers))

    def clear_wallpapers(self):
        self.wallpaper_view.set_wallpapers([])
        self.update_wallpaper_count(0)

    def update_wallpaper_count(self, count):
        self.statusbar.pop(self.context_id)
        return self.statusbar.push(self.context_id, 'Wallpapers: %s' % count)

    def get_limit_adjustment(self):
        wallpapers = self.app.wally.wallpapers.get(self.get_display_type(), [])
        return gtk.Adjustment(100, 1, len(wallpapers), 1, 10)

    def get_target(self):
        return self.displays.get_active()

    def get_display_type(self):
        return self.app.wally.display_type[self.get_target()]

    # WIDGETS {{{3
    def _get_window_content(self): #{{{4
        vbox = gtk.VBox()
        vbox.pack_start(self._get_menubar(), expand=False)
        vbox.pack_start(self._get_search(), expand=False)
        vbox.pack_start(self._get_viewport())
        vbox.pack_end(self._get_statusbar(), expand=False)
        return vbox

    def _get_statusbar(self): #{{{4
        self.statusbar = gtk.Statusbar()
        self.context_id = self.statusbar.get_context_id(__appname__)
        return self.statusbar

    def _get_viewport(self): #{{{4
        scrolled = gtk.ScrolledWindow()
        scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.wallpaper_view = WallpaperIconView(app=self.app)
        self.wallpaper_view.connect('selection-changed', self.on_wallpaper_view_selection_changed)
        scrolled.add_with_viewport(self.wallpaper_view)
        return scrolled

    def _get_search(self): #{{{4
        hbox = gtk.HBox()
        self.displays = gtk.combo_box_new_text()
        for n, m in enumerate(self.app.wally.monitors):
            self.displays.append_text("Display %s" % n)
        self.displays.set_active(0)
        self.displays.connect('changed', self.on_displays_changed)
        hbox.pack_start(self.displays, expand=False, fill=False)
        self.search_entry = gtk.Entry()
        hbox.pack_start(self.search_entry)
        clear = gtk.Button()
        clear.add(gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
        hbox.pack_start(clear, expand=False, fill=False)
        self.search_button = gtk.Button('Search')
        self.search_button.set_image(gtk.image_new_from_stock(gtk.STOCK_FIND, gtk.ICON_SIZE_MENU))
        self.search_button.connect('clicked', self.on_search_button_clicked)
        self.search_entry.connect_object('activate', gtk.Button.clicked, self.search_button)
        clear.connect('clicked', self.on_search_clear_clicked)
        hbox.pack_start(self.search_button, expand=False, fill=False)
        self.search_limit = gtk.SpinButton()
        self.search_limit.set_adjustment(self.get_limit_adjustment())
        self.search_limit.set_numeric(True)
        hbox.pack_start(self.search_limit, expand=False, fill=False)
        return hbox

    def _get_menubar(self): #{{{4
        mb = gtk.MenuBar()
        mb.add(self._get_file_menu())
        mb.add(self._get_wallpaper_menu())
        mb.add(self._get_options_menu())
        mb.add(self._get_help_menu())
        return mb

    def _get_help_menu(self): #{{{4
        m = gtk.MenuItem('_Help')
        sm = gtk.Menu()
        mi_about = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        mi_about.connect('activate', self.on_about_menuitem_activate)
        sm.add(mi_about)
        m.set_submenu(sm)
        return m

    def _get_options_menu(self): #{{{4
        m = gtk.MenuItem('_Options')
        sm = gtk.Menu()
        mi_dirs = gtk.MenuItem('_Directories')
        mi_dirs.connect('activate', self.on_directories_menuitem_activate)
        sm.add(mi_dirs)
        mi_ex = gtk.MenuItem('_Exclusions')
        mi_ex.connect('activate', self.on_exclusions_menuitem_activate)
        sm.add(mi_ex)
        mi_color = gtk.MenuItem('_Background Color')
        mi_color.connect('activate', self.on_color_menuitem_activate)
        sm.add(mi_color)
        m.set_submenu(sm)
        return m

    def _get_wallpaper_menu(self): #{{{4
        m = gtk.MenuItem('_Wallpaper')
        sm = gtk.Menu()
        self.selected_menuitem = self._get_wallpaper_menuitem('Set _Selected', self.on_selected_menuitem_activate)
        self.selected_menuitem.set_sensitive(False)
        sm.add(self.selected_menuitem)
        sm.add(self._get_wallpaper_menuitem('Set _Random', self.on_random_menuitem_activate))
        sm.add(self._get_wallpaper_menuitem('Set _Next', self.on_next_menuitem_activate))
        sm.add(self._get_wallpaper_menuitem('Set _Previous', self.on_prev_menuitem_activate))
        m.set_submenu(sm)
        return m

    def _get_file_menu(self): #{{{4
        fm = gtk.MenuItem('_File')
        sm = gtk.Menu()
        mi_quit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        mi_quit.connect_object('activate', gtk.Window.destroy, self)
        sm.add(mi_quit)
        fm.set_submenu(sm)
        return fm

    def _get_wallpaper_menuitem(self, label, cb): #{{{4
        mi = gtk.MenuItem(label)
        mi.connect('activate', cb)
        return mi

    # HANDLERS {{{3
    def on_selected_menuitem_activate(self, menuitem): #{{{4
        w = self.wallpaper_view.get_selected()
        self.app.wally.display[self.get_target()] = w
        self.app.wally.refresh_display()

    def on_displays_changed(self, combobox): #{{{4
        self.search_limit.set_adjustment(self.get_limit_adjustment())
        self.clear_wallpapers()

    def on_random_menuitem_activate(self, menuitem): #{{{4
        self.app.wally.change_random(self.get_target())
        self.app.wally.refresh_display()

    def on_next_menuitem_activate(self, menuitem): #{{{4
        self.app.wally.change_next(self.get_target())
        self.app.wally.refresh_display()

    def on_prev_menuitem_activate(self, menuitem): #{{{4
        self.app.wally.change_prev(self.get_target())
        self.app.wally.refresh_display()

    def on_directories_menuitem_activate(self, widget): #{{{4
        directories = {}
        for n, wt in enumerate(WALLPAPER_TYPES):
            directories[wt] = self.app.wally.config.directories.get(wt, [])
        dialog = DirectoriesDialog(directories, parent=self)
        if dialog.run() != gtk.RESPONSE_OK: return
        for wt, dirs in dialog.get_directories().iteritems():
            if not dirs: continue
            self.app.wally.config.directories[wt] = dirs
        self.app.wally.config.write()

    def on_exclusions_menuitem_activate(self, widget): #{{{4
        dialog = ExclusionsDialog(self.app.wally.config.exclusions, parent=self)
        if dialog.run() != gtk.RESPONSE_OK: return
        self.app.wally.config.exclusions = dialog.get_exclusions()
        self.app.wally.config.write()

    def on_color_menuitem_activate(self, widget): #{{{4
        color = rgb8_to_rgb16(self.app.wally.config.background_color)
        color = BackgroundColorDialog(gtk.gdk.Color(*color)).run()
        if not color: return
        self.app.wally.config.background_color = rgb16_to_rgb8((color.red, color.green, color.blue))
        self.app.wally.config.write()

    def on_about_menuitem_activate(self, widget): #{{{4
        AboutDialog(
                name=__appname__,
                authors=[__author__],
                website=__url__,
                license=__license__,
                logo=get_icon('logo.svg'),
                ).run()

    def on_search_button_clicked(self, widget): #{{{4
        self.refresh_wallpapers(self.search_entry.get_text())

    def on_search_clear_clicked(self, widget): #{{{4
        self.search_entry.set_text('')
        self.wallpaper_view.clear()
        self.update_wallpaper_count(0)

    def on_wallpaper_view_selection_changed(self, widget): #{{{4
        self.selected_menuitem.set_sensitive(bool(self.wallpaper_view.get_selected()))



class WallyGTK(object): #{{{1

    def __init__(self):
        self.wally = Wally()
        self.thumbs = Thumbnails()
        self.window = MainWindow(self)
        self.window.connect('destroy', gtk.main_quit)

    def get_thumbnail(self, wallpaper):
        return self.thumbs.get_normal(wallpaper)
