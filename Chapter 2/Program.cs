using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace modification
{
    public class SalaryCalculator
    {
        //метод для расчета зп до вычетов
        public double CalculateBaseSalary(double hours, double rate)
        {

            return hours * rate;
        }
        //метод для расчета с учетом налога в 13%
        public double CalculateNetSalary(double hours, double rate)
        {
            double gross = CalculateBaseSalary(hours, rate);
            return gross * 0.87;
        }

    }
    //модифицируемый модуль добавляем премию и поэтапный налог 

    public class ModificationSalaryCalculator : SalaryCalculator
    {
        //переопределяем метод расчета зарплаты с учетом новых правил 
        public new double CalculateNetSalary(double hours, double rate, double bonus = 0)
        {
            double gross = CalculateBaseSalary(hours, rate);
            gross *= bonus;
            double tax = 0;
            if (gross <= 25000)
            {
                gross = gross * 0.9;
            }
            else

            {
                gross = gross * 0.87;
            }
            return gross;

        }
    }


    internal class Program
    {
        static void Main(string[] args)
        {
            SalaryCalculator oldCalc = new SalaryCalculator();
            double oldNet = oldCalc.CalculateNetSalary(160, 250);
            Console.WriteLine($"Старая версия: {oldNet}");

            ModificationSalaryCalculator newCalc = new ModificationSalaryCalculator();
            double newNet = newCalc.CalculateNetSalary(160, 250, 3000);
            Console.WriteLine($"Новая версия: {newNet}");

            double noBonus = newCalc.CalculateNetSalary(160, 250);
            Console.WriteLine($"Без премии: {noBonus}");
        }
    }
}
