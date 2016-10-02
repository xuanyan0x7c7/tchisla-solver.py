from quadratic import Quadratic
from expression import Expression

__all__ = ["global_config"]

global_config = {
	"verbose": False
}

specials = {
	"integral": {},
	"rational": {},
	"quadratic": {
		7: {
			3: [
				# sqrt(14!+7!)
				(Quadratic.sqrt(Quadratic(87178296240)), Expression.sqrt(Expression.add(Expression.factorial(14), Expression.factorial(7))))
			]
		},
		8: {
			2: [
				(Quadratic.sqrt(Quadratic(80640)), Expression.sqrt(Expression.add(Expression.factorial(8), Expression.factorial(8))))
			]
		}
	}
}
