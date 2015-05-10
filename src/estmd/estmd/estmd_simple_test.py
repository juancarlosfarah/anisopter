from estmd import ESTMD

input_directory = "test.avi"
e = ESTMD()
e.open_movie(input_directory)
e.run(by_frame=True)
r = e.create_list_of_arrays()

print "Done testing!"
