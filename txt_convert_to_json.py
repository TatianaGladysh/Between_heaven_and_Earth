with open("levels/polyclinic.txt") as f:
    t = f.read().split(' \\\n')

t = [b.split("\n") for b in t]
print('\n'.join(map(lambda b: '\n'.join(f'      "{r.strip()}",' for r in b[:-1]) + '\n', t)))
