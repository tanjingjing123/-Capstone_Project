import collections
from functools import partial
import tkinter as tk
from translate import Translator
import webbrowser


class HyperlinkManager:
    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyper", foreground="blue", underline=1)
        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)
        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(tk.CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return

def load_music_list():
    music_database = collections.defaultdict(list)
    music_labels = collections.defaultdict(list)
    with open('musics') as music_file:
        music_type = ''
        labels = []
        for line in music_file:
            line = line.strip()
            if not line:
                for label in labels:
                    music_labels[label] += music_database[music_type]
                labels = []
                continue
            if '+' in line:
                labels.append(line.replace('+', '').strip().lower())
            elif '~' in line:
                line = line.replace('~', '')
                arr = line.split('|')
                music_database[music_type].append((arr[0].lower().strip(), arr[1].strip(), arr[2].strip()))
            else:
                music_type = line.lower()
    return music_database, music_labels


def hamming_distance(string1, string2):
    distance = 0
    l = min(len(string1), len(string2))
    for i in range(l):
        if string1[i] != string2[i]:
            distance += 1
    return distance


def recommend(string, music_database, music_labels):
    string = string.lower()
    if string in music_labels:
        return music_labels[string]
    if string in music_database:
        return music_database[string]
    result = []
    for arr in music_database.values():
        for song, author, link in arr:
            if string in song or string in author.lower():
                result.append((song, author, link))
    if result:
        return result
    min_distance = -1
    best_category = None
    for category in music_database.keys():
        distance = hamming_distance(string, category)
        if min_distance == -1 or distance < min_distance:
            min_distance = distance
            best_category = category
    return music_database[best_category]


def activate(calculated_label):
    main_window = tk.Tk()
    main_window.title('Music Recommendation')
    main_window.geometry("800x600")
    main_window.configure(bg='grey')

    display_entry = tk.Text(main_window,
                            height = 45,
                            width = 110,
                            bg='light grey',
                            fg='black',
                            state=tk.DISABLED)
    display_entry.grid(column=0, row=4)
    clickable_link = HyperlinkManager(display_entry)

    music_list, music_by_labels = load_music_list()
    result = recommend(calculated_label, music_list, music_by_labels)
    display_entry.config(state=tk.NORMAL)
    display_entry.delete(1.0, tk.END)
    for num, data in enumerate(result):
        display_entry.insert(tk.END, 'Music ' + str(num + 1) + '\n')
        display_entry.insert(tk.END, '- Name: ' + data[0] + '\n')
        display_entry.insert(tk.END, '- Author: ' + data[1] + '\n')
        display_entry.insert(tk.END, '- Link: ' + data[2] + '\n',
                             clickable_link.add(partial(webbrowser.open, data[2])))
        display_entry.insert(tk.END, '\n')
    display_entry.bind("<Button-2>", lambda event: webbrowser.open(display_entry.cget("text")))
    display_entry.config(state=tk.DISABLED)

    main_window.mainloop()


if __name__ == '__main__':
    activate('Anger')
    # root = tk.Tk()
    # root.title('Music Recommendation')
    # root.geometry("600x400")
    # root.configure(bg='grey')
    # hint = tk.Label(root, text='Enter keyword',
    #                 font=('calibre',
    #                       10, 'bold'))
    # hint.grid(column=0, row=0, sticky="nsew")
    # keyword = tk.StringVar()
    # keyword_entry = tk.Entry(root,
    #                       textvariable=keyword, font=('calibre', 10, 'normal'))
    # keyword_entry.grid(column=0, row=1, sticky="nsew")
    #
    # def submit():
    #     global keyword, hyperlink, translator
    #     keyword = keyword_entry.get()
    #     keyword = translator.translate(keyword)
    #
    #     translated_entry.config(state=tk.NORMAL)
    #     translated_entry.delete(1.0, tk.END)
    #     translated_entry.insert(tk.END, 'Translated:\n')
    #     translated_entry.insert(tk.END, keyword)
    #     translated_entry.config(state=tk.DISABLED)
    #
    #     music_list, music_by_labels = load_music_list()
    #     result = recommend(keyword, music_list, music_by_labels)
    #     result_entry.config(state=tk.NORMAL)
    #     result_entry.delete(1.0, tk.END)
    #     for num, data in enumerate(result):
    #         result_entry.insert(tk.END, 'Music ' + str(num + 1) + '\n')
    #         result_entry.insert(tk.END, '- Name: ' + data[0] + '\n')
    #         result_entry.insert(tk.END, '- Author: ' + data[1] + '\n')
    #         result_entry.insert(tk.END, '- Link: ' + data[2] + '\n',
    #                             hyperlink.add(partial(webbrowser.open, data[2])))
    #         result_entry.insert(tk.END, '\n')
    #     result_entry.bind("<Button-2>", lambda event: webbrowser.open(result_entry.cget("text")))
    #     result_entry.config(state=tk.DISABLED)
    #
    # button = tk.Button(root, text='Submit',
    #                     command=submit)
    # button.grid(column=0, row=2, sticky="nsew")
    #
    # # use tkinter to make the user interface
    # translated_entry = tk.Text(root,
    #                        height = 2,
    #                        width = 5,
    #                        bg='grey',
    #                        fg='black',
    #                        font=('calibre', 10, 'normal'),
    #                        state=tk.DISABLED)
    # translated_entry.grid(column=0, row=3, sticky="nsew")
    #
    # result_entry = tk.Text(root,
    #                        height = 20,
    #                        width = 40,
    #                        bg='light grey',
    #                        fg='black',
    #                        state=tk.DISABLED)
    # result_entry.grid(column=0, row=4)
    # hyperlink = HyperlinkManager(result_entry)
    #
    # translator = Translator(to_lang='en', from_lang='zh')
    #
    # root.mainloop()
