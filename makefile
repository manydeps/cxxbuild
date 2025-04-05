all: run_demo

clean: clean_demo

run_demo:
	echo "\n\nRUN DEMO 1\n\n"
	uv run cxxbuild demo/project1
	echo "\n\nRUN DEMO 2\n\n"
	uv run cxxbuild demo/project2
	echo "\n\nRUN DEMO 3\n\n"
	uv run cxxbuild demo/project3
	echo "\n\nRUN DEMO 4\n\n"
	uv run cxxbuild demo/project4 --c++20
	echo "\n\nRUN DEMO 5\n\n"
	uv run cxxbuild demo/project5
	echo "\n\nRUN DEMO 6\n\n"
	uv run cxxbuild demo/project6

clean_demo:
	rm -rf demo/project1/build
	rm -rf demo/project2/build
	rm -rf demo/project3/build
	rm -rf demo/project4/build
	rm -rf demo/project5/build
	rm -rf demo/project6/build
