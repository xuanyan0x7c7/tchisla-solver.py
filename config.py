from quadratic import Quadratic
from expression import Expression

__all__ = ["global_config"]

global_config = {
	"verbose": False
}

limits = {
	"integral": {
		"default": {
			"max": 1 << 64,
			"max_digits": 64,
			"max_concat": 20,
			"max_factorial": 20
		}
	},
	"rational": {
		"default": {
			"max": 1 << 32,
			"max_digits": 32,
			"max_concat": 20,
			"max_factorial": 12
		}
	},
	"quadratic": {
		"default": {
			"max": 1 << 16,
			"max_digits": 16,
			"max_concat": 5,
			"max_factorial": 8,
			"max_quadratic_power": 1,
		}
	}
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
