import jaraco.windows.mmap as mmap

def test_mmap_simple():
	map = mmap.MemoryMap('foo', 50)
	with map:
		map.write('abc')
		map.write('def')
		map.seek(0)
		assert map.read(4) == 'abcd'
		assert map.read(2) == 'ef'
