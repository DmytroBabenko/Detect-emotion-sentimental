class Utils:


    @staticmethod
    def read_links(filepath):
        lines = []
        with open(filepath) as fp:
            for cnt, line in enumerate(fp):
                lines.append(line)

        return lines





if __name__ == "__main__":
    filepath = "../data/links/odesa-hotel-reviews.txt"

    lines = Utils.read_links(filepath)

    a = 10
