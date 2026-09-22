"""Exact unit-capacity matching and nested-window certificate scheduling."""
def matching(edges,slots):
    edges=[sorted(set(e)) for e in edges];owner={}
    assert all(0<=s<len(slots) for e in edges for s in e)
    def augment(a,seen):
        for s in edges[a]:
            if s in seen:continue
            seen.add(s)
            if s not in owner or augment(owner[s],seen):owner[s]=a;return True
        return False
    for a in range(len(edges)):augment(a,set())
    assigned={a:slots[s] for s,a in owner.items()}
    if len(assigned)==len(edges):return dict(feasible=True,assignment=assigned,deficient_jobs=[],neighbor_slots=0)
    # Alternating closure from unmatched jobs gives a Hall-deficient set.
    reached=set(range(len(edges)))-set(assigned);queue=list(reached);neighbors=set()
    while queue:
        a=queue.pop()
        for s in edges[a]:
            neighbors.add(s)
            if s in owner and owner[s] not in reached:reached.add(owner[s]);queue.append(owner[s])
    assert len(neighbors)<len(reached)
    return dict(feasible=False,assignment=assigned,deficient_jobs=sorted(reached),neighbor_slots=len(neighbors))

def known_lifetimes(releases,lifetimes,target,capacities):
    assert len(releases)==len(lifetimes) and all(x>0 for x in lifetimes)
    assert all(b>=0 and int(b)==b for b in capacities.values())
    lower=[max(r,target-life+1) for r,life in zip(releases,lifetimes)]
    slots=sorted(t for t,b in capacities.items() if t<=target for _ in range(b))
    schedule={};unused=slots.copy()
    for a in sorted(range(len(lower)),key=lambda a:(-lower[a],a)):
        if not unused or unused[-1]<lower[a]:
            s=lower[a];jobs=[j for j,l in enumerate(lower) if l>=s];cap=sum(t>=s for t in slots)
            assert len(jobs)>cap
            return dict(feasible=False,assignment=schedule,threshold=s,jobs=jobs,capacity=cap)
        schedule[a]=unused.pop()
    return dict(feasible=True,assignment=schedule)
