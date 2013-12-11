import pickle
QUERY = '家庭菜園　始める　方法'
DIR = 'gardening'

if __name__ == '__main__':
    pages = []
    for i in range(30):
        f = open('pickled_pages_before_build' + DIR + '_page_' + str(i) + '.pkl', 'rb')
        pages.append(pickle.load(f))
        f.close()

    for page in pages:
        page.build_heading_tree()

