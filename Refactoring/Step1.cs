using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Schema;

namespace Step1
{
    internal class step1
    {
        string _connection;
        public class UserWithOrdersDto
        {

        }
        public List<UserWithOrdersDto> GetUserWithOrders()
        {
            //using for auto close
            using (var connection = new SqlConnection(_connection))
            {
                connection.Open();
                const string usersSql = "SELECRT Id,Name, From Users";
                using (var userCmd = new SqlCommand(usersSql, connection))
                using (var userReader = userCmd.ExecuteReader())
                {
                    while (userReader.Read())
                    {
                        var userid = userReader.GetInt32(userReader.GetOrdinal("id"));
                    }
                }
            }
        }
    }
}