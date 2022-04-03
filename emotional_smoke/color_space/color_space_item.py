class ColorSpaceItem(object):
    def __init__(self, lab_data, rgb_data):
        self.lab_color = lab_data
        self.rgb_color = rgb_data

    def __len__(self):
        return len(self.lab_color)

    def __getitem__(self, i):
        return self.lab_color[i]

    def __repr__(self):
        return 'Item({}, {}, {}, {})'.format(self.lab_color[0], self.lab_color[1], self.lab_color[2], self.rgb_color)



