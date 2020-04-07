#define configfile = config.t

main():
	config.load()
	population p = new population()
	while True:
		p.aproximate_fittness()
		p =  new population(a)



class population:

	int population_size = config.population_size()
	int discard = config.discard()
	table members[N]	
	

	__init__(): //constructs population with random members
		while (i in range 0,population_size):
			member m = new member
			members.add(new member)
	
	__init__(population p): //constructs population by mutating given population
		//sorting members by fittness
		p.sort_members_by_fittness()
		
		//discarding worst members
		discarded members = discard/population_size
		p.discard(discarded_members)

		//filling population
		fittness_sum = p.fittness_sum
		for (int i; members.not_full(); i++):
			member m = population.get(i)
			n_mutations = (m.fittness()/fittness_sum)/discarded_members
			
			//adding this member
			members.add(a)

			//adding mutations of member, number based on fittness
			for n_mutations:
				members.add(a.mutate)



class member: //this is a member, contains solution to problem
	int fittness
	
	test_fittness():
		//tests fittness of member with
		//use of io class
	
	fittness():
		//return fittness
	
	__init__():
		//creates random solution


class config:

	load(): //loads data from file 
		read(configfile)


	//GET funtions:
	discard():
		return discard
	population_size():
		return population_size




class io: //this class writes and reads STM pins 
	write_pin()
	read_pin()
