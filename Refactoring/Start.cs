using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Schema;

namespace internetShop_до_рефакторинга_
{
    public class UserService
    {
        private readonly SqlConnection _connection;
        public UserService(SqlConnection connection)
        {
            _connection = connection;
        }
        public List<object> GetUsersWithOrders()
        {
            var result = new List<object>();
            var userCmd = new SqlCommand("SELECT * FROM USERS", _connection);
            var userReader = userCmd.ExecuteReader();
            while (userReader.Read())
            {
                var userID = userReader.GetInt32(0);
                var userName = userReader.GetString(1);
                var orderCmd = new SqlCommand($"SELECT * FROM ORDERS where userID={userID}", _connection);
                var orderReader = orderCmd.ExecuteReader();
                var orders = new List<object>();
                while (orderReader.Read())
                {
                    orders.Add(new { orderID = orderReader.GetInt32(0), Total = orderReader.GetDecimal(2) });
                }
                orderReader.Close();
                result.Add(new
                {
                    UserId = userID,
                    UserName = userName,
                    Order = orders
                });
            }
            userReader.Close();
            return result;
        }
    }
    internal class Program
    {
        static void Main(string[] args)
        {
        }
    }
}
