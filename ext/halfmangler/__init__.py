#!/usr/bin/python

class CElement:
	def __init__(self, v = ""):
		self.separator = ""
		self.children = []
		self.members = []
		self.parent = None
		self.val = v

BLOCK_STARTS = ['N', 'I', 'X', "sr"]
BLOCK_ENDS = ['E']
block_h = 0

def is_digit(x):
	return ord('0') <= ord(x) <= ord('9')

def get_simple_name(x):
	global block_h

	stds = {
		"S_": "S_",
		"SB": "SB_",
		"St": "std",
		"Sa": "std::allocator",
		"Sb": "std::basic_string",
		"Ss": "std::basic_string<char, std::char_traits<char>, std::allocator<char> >",
		"Si": "std::basic_istream<char, std::char_traits<char> >",
		"So": "std::basic_ostream<char, std::char_traits<char> >",
		"Sd": "std::basic_iostream<char, std::char_traits<char> >",
		"T_": "T"
		}

	length = 0
	digits = 0

	# Add substitutes
	for j in xrange(10):
		stds["S%d" % j] = "S%d_" % j

	for c in x:
		if not is_digit(c):
			break

		digits += 1
		length = length * 10 + int(c)

	if length != 0:
		s = x[digits:digits + length]
		print "\t" * (block_h) + "Simple [%s] Symbol length %d" % (s, length)
		return s, digits + length

	abbr = x[:2]

	if abbr in stds:
		print "\t" * (block_h) + "Got Simple abbr [%s]" % abbr
		length = len(abbr)

		if (abbr[0] == 'S') and (is_digit(abbr[1])):
			length += 1

		return stds[abbr], length

	if x == "m":
		return "unsigned int", 1

	return None

def get_sym(elem):
	global block_h

	print "\t" * block_h + "children = %d" % len(elem.children)
	i = 0

	while i < len(elem.val):
		symbol = get_simple_name(elem.val[i:])

		if symbol is not None:
			symbol, length = symbol
			i += length
			elem.members.append(symbol)
			continue

		sym = find_sym(elem.val[i:], BLOCK_STARTS)

		if sym is not None:
			print "\t" * block_h + elem.val
			child = elem.children[0]

			# Update children list
			elem.children = elem.children[1:]

			block_h += 1
			elem.members.append("<%s>" % get_sym(child))
			block_h -= 1

			i += len(child.val)
			print "\t" * (block_h) + elem.members[-1]
			continue
		i += 1

	if elem.separator == 'N':
		return "::".join(elem.members).replace("::<", "<")
	else:
		return ",".join(elem.members).replace(",<", "<")

def find_sym(x, symbols):
	global block_h

	for s in symbols:
		if s == x[:len(s)]:
			return s

	return None

def demangle(x):
	global block_h

	print x
	# If it isn't C++ mangled name
	if x[:2] != "_Z":
		return x

	# Get rid of C++ Annotation for demangled name start
	x = x[2:]

	BLOCKS = []
	ELEMENTS = []
	cur_elems = []

	i = 0
	while i < len(x):
		# Find block starts
		s = find_sym(x[i:], BLOCK_STARTS)

		if s is not None:
			# print "\t" * block_h + "Block start %s %s" % (s, x[i:])
			print "\t" * block_h + "Block start %s" % (s)
			block_h += 1

			BLOCKS.append((x[i:i+len(s)], i + len(s)))
			i += len(s)
			continue

		symbol = get_simple_name(x[i:])

		if symbol is not None:
			symbol, length = symbol

			i += length
			continue

		# Find block ends
		s = find_sym(x[i:], BLOCK_ENDS)

		if s is not None:
			# Create new element
			block_type, start = BLOCKS.pop()
			e = CElement(x[start:i])
			e.separator = block_type

			block_h -= 1
			print "\t" * block_h + "Block end %s" % e.val


			if cur_elem is not None:
				e.children.append(cur_elem)
				print "\t" * block_h + "children = %d" % len(e.children)

			cur_elem = e
			if len(BLOCKS) == 0:
				ELEMENTS.append(cur_elem)
				cur_elem = None

			i += len(s)
			continue

		i += 1

	print "=" * 16
	for elem in ELEMENTS:
		print get_sym(elem)

if __name__ == "__main__":
	# print demangle("_ZN4Math13subtractExactImEENSt6__ndk19enable_ifIXsr11is_unsignedIT_EE5valueES3_E4typeES3_S3_")
	print demangle("_ZNSt6__ndk16vectorINS_9sub_matchIPKcEENS_9allocatorIS4_EEE6assignIPS4_EENS_9enable_ifIXaasr21__is_forward_iteratorIT_EE5valuesr16is_constructibleIS4_NS_15iterator_traitsISB_E9referenceEEE5valueEvE4typeESB_SB_")
